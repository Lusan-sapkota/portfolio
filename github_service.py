"""
GitHub API Service with Caching
Handles GitHub API requests with intelligent caching and error handling
"""

import os
import requests
import time
from datetime import datetime, timedelta
from flask import current_app
from flask_caching import Cache
import json
import hashlib

class GitHubService:
    def __init__(self):
        self.cache = None
        self.base_url = "https://api.github.com"
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Portfolio-Website-v1.0'
        }
        
        # Add GitHub token if available
        github_token = os.getenv('GITHUB_TOKEN')
        if github_token:
            self.headers['Authorization'] = f'token {github_token}'
        
        # Mock data mode for development
        self.mock_mode = os.getenv('GITHUB_MOCK_MODE', 'False').lower() == 'true'
        
        # Real repositories for demo (when mock_mode is False)
        self.demo_repos = {
            'lusansapkota/portfolio': 'microsoft/vscode',  # Use VSCode as demo
            'lusansapkota/task-api': 'facebook/react',
            'lusansapkota/ecommerce-mobile': 'vercel/next.js',
            'lusansapkota/analytics-dashboard': 'django/django',
            'lusansapkota/docker-pipeline': 'docker/compose',
            'lusansapkota/web-utils': 'lodash/lodash',
            'lusansapkota/pdf-manager': 'mozilla/pdf.js'
        }
    
    def init_cache(self, app):
        """Initialize cache with app context"""
        # Try Redis first, fallback to simple cache
        try:
            redis_url = os.getenv('REDIS_URL')
            if redis_url:
                cache_config = {
                    'CACHE_TYPE': 'RedisCache',
                    'CACHE_REDIS_URL': redis_url,
                    'CACHE_DEFAULT_TIMEOUT': 3600  # 1 hour default
                }
            else:
                # Fallback to simple in-memory cache
                cache_config = {
                    'CACHE_TYPE': 'SimpleCache',
                    'CACHE_DEFAULT_TIMEOUT': 3600
                }
            
            self.cache = Cache(config=cache_config)
            self.cache.init_app(app)
            print(f"GitHub Service: Cache initialized with {cache_config['CACHE_TYPE']}")
            
            if self.mock_mode:
                print("GitHub Service: Running in MOCK MODE - using fake data")
            else:
                print("GitHub Service: Using real GitHub API with demo repositories")
            
        except Exception as e:
            print(f"Cache initialization error: {e}")
            # Fallback to simple cache
            self.cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
            self.cache.init_app(app)
    
    def _get_cache_key(self, username, repo):
        """Generate cache key for repository"""
        return f"github_repo:{username}:{repo}"
    
    def _get_error_cache_key(self, username, repo):
        """Generate cache key for errors"""
        return f"github_error:{username}:{repo}"
    
    def _is_valid_repo_format(self, username, repo):
        """Validate repository format"""
        if not username or not repo:
            return False
        
        # Check for valid characters
        import re
        if not re.match(r'^[a-zA-Z0-9._-]+$', username):
            return False
        if not re.match(r'^[a-zA-Z0-9._-]+$', repo):
            return False
            
        return True
    
    def _get_mock_data(self, username, repo):
        """Generate mock GitHub data for development"""
        import random
        
        # Create consistent mock data based on repo name
        seed = hash(f"{username}/{repo}")
        random.seed(seed)
        
        mock_data = {
            'name': repo,
            'full_name': f"{username}/{repo}",
            'description': f"Mock repository for {repo} - This is sample data for development",
            'html_url': f"https://github.com/{username}/{repo}",
            'clone_url': f"https://github.com/{username}/{repo}.git",
            'ssh_url': f"git@github.com:{username}/{repo}.git",
            'stargazers_count': random.randint(10, 1000),
            'forks_count': random.randint(5, 200),
            'watchers_count': random.randint(10, 1000),
            'size': random.randint(100, 50000),
            'language': random.choice(['Python', 'JavaScript', 'TypeScript', 'Java', 'Go', 'Rust', 'PHP']),
            'topics': random.sample(['web', 'api', 'python', 'javascript', 'react', 'django', 'flask', 'nodejs'], k=random.randint(2, 4)),
            'created_at': '2023-01-15T10:30:00Z',
            'updated_at': '2024-12-15T14:25:00Z',
            'pushed_at': '2024-12-20T09:15:00Z',
            'is_private': False,
            'is_fork': False,
            'default_branch': 'main',
            'license': random.choice([None, 'MIT', 'Apache-2.0', 'GPL-3.0']),
            'homepage': None,
            'cached_at': datetime.utcnow().isoformat(),
            'api_rate_limit_remaining': '4999',
            'api_rate_limit_reset': str(int(time.time()) + 3600),
            'mock_data': True  # Flag to indicate this is mock data
        }
        
        return mock_data
    
    def get_repository_data(self, username, repo, force_refresh=False):
        """
        Get repository data from GitHub API with caching
        
        Args:
            username (str): GitHub username
            repo (str): Repository name
            force_refresh (bool): Force refresh from API
            
        Returns:
            dict: Repository data or None if error/not found
        """
        if not self._is_valid_repo_format(username, repo):
            print(f"Invalid repository format: {username}/{repo}")
            return None
        
        # Handle mock mode
        if self.mock_mode:
            print(f"Mock mode: Generating fake data for {username}/{repo}")
            mock_data = self._get_mock_data(username, repo)
            # Cache mock data for consistency
            if self.cache:
                cache_key = self._get_cache_key(username, repo)
                self.cache.set(cache_key, mock_data, timeout=86400)  # Cache for 24 hours
            return mock_data
        
        # Check for demo repository mapping
        original_repo = f"{username}/{repo}"
        if original_repo in self.demo_repos:
            demo_repo = self.demo_repos[original_repo]
            demo_username, demo_repo_name = demo_repo.split('/', 1)
            print(f"Using demo repository {demo_repo} for {original_repo}")
            return self._get_demo_repository_data(username, repo, demo_username, demo_repo_name, force_refresh)
        
        cache_key = self._get_cache_key(username, repo)
        error_cache_key = self._get_error_cache_key(username, repo)
        
        # Check if we have a cached error (don't retry failed requests for 6 hours)
        if not force_refresh and self.cache:
            cached_error = self.cache.get(error_cache_key)
            if cached_error:
                print(f"Repository {username}/{repo} in error cache, skipping API call")
                return None
        
        # Check cache first
        if not force_refresh and self.cache:
            cached_data = self.cache.get(cache_key)
            if cached_data:
                print(f"Using cached data for {username}/{repo}")
                return cached_data
        
        # Fetch from API
        return self._fetch_from_api(username, repo, cache_key, error_cache_key)
    
    def _get_demo_repository_data(self, original_username, original_repo, demo_username, demo_repo, force_refresh=False):
        """Get data from a demo repository but return it as if it belongs to the original repo"""
        cache_key = self._get_cache_key(original_username, original_repo)
        error_cache_key = self._get_error_cache_key(original_username, original_repo)
        
        # Check cache first
        if not force_refresh and self.cache:
            cached_data = self.cache.get(cache_key)
            if cached_data:
                print(f"Using cached demo data for {original_username}/{original_repo}")
                return cached_data
        
        # Fetch demo repository data
        demo_data = self._fetch_from_api(demo_username, demo_repo, f"demo_{cache_key}", f"demo_{error_cache_key}")
        
        if demo_data:
            # Modify the data to appear as if it belongs to the original repository
            modified_data = demo_data.copy()
            modified_data['name'] = original_repo
            modified_data['full_name'] = f"{original_username}/{original_repo}"
            modified_data['html_url'] = f"https://github.com/{original_username}/{original_repo}"
            modified_data['clone_url'] = f"https://github.com/{original_username}/{original_repo}.git"
            modified_data['ssh_url'] = f"git@github.com:{original_username}/{original_repo}.git"
            modified_data['demo_data'] = True
            modified_data['demo_source'] = f"{demo_username}/{demo_repo}"
            
            # Cache the modified data
            if self.cache:
                self.cache.set(cache_key, modified_data, timeout=7200)
            
            return modified_data
        
        return None
    
    def _fetch_from_api(self, username, repo, cache_key, error_cache_key):
        """Fetch data from GitHub API"""
        api_url = f"{self.base_url}/repos/{username}/{repo}"
        
        try:
            print(f"Fetching GitHub data for {username}/{repo}")
            response = requests.get(api_url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Process and clean the data
                processed_data = {
                    'name': data.get('name'),
                    'full_name': data.get('full_name'),
                    'description': data.get('description'),
                    'html_url': data.get('html_url'),
                    'clone_url': data.get('clone_url'),
                    'ssh_url': data.get('ssh_url'),
                    'stargazers_count': data.get('stargazers_count', 0),
                    'forks_count': data.get('forks_count', 0),
                    'watchers_count': data.get('watchers_count', 0),
                    'size': data.get('size', 0),
                    'language': data.get('language'),
                    'topics': data.get('topics', []),
                    'created_at': data.get('created_at'),
                    'updated_at': data.get('updated_at'),
                    'pushed_at': data.get('pushed_at'),
                    'is_private': data.get('private', False),
                    'is_fork': data.get('fork', False),
                    'default_branch': data.get('default_branch', 'main'),
                    'license': data.get('license', {}).get('name') if data.get('license') else None,
                    'homepage': data.get('homepage'),
                    'cached_at': datetime.utcnow().isoformat(),
                    'api_rate_limit_remaining': response.headers.get('X-RateLimit-Remaining'),
                    'api_rate_limit_reset': response.headers.get('X-RateLimit-Reset')
                }
                
                # Cache successful response for 2 hours
                if self.cache:
                    self.cache.set(cache_key, processed_data, timeout=7200)
                    # Clear any error cache
                    self.cache.delete(error_cache_key)
                
                print(f"Successfully fetched and cached data for {username}/{repo}")
                return processed_data
                
            elif response.status_code == 404:
                print(f"Repository {username}/{repo} not found (404)")
                # Cache 404 errors for 6 hours to avoid repeated requests
                if self.cache:
                    error_data = {
                        'error': 'not_found',
                        'status_code': 404,
                        'message': 'Repository not found',
                        'cached_at': datetime.utcnow().isoformat()
                    }
                    self.cache.set(error_cache_key, error_data, timeout=21600)  # 6 hours
                return None
                
            elif response.status_code == 403:
                print(f"GitHub API rate limit exceeded or access forbidden for {username}/{repo}")
                # Cache rate limit errors for 1 hour
                if self.cache:
                    error_data = {
                        'error': 'rate_limit_or_forbidden',
                        'status_code': 403,
                        'message': 'Rate limit exceeded or access forbidden',
                        'cached_at': datetime.utcnow().isoformat(),
                        'rate_limit_reset': response.headers.get('X-RateLimit-Reset')
                    }
                    self.cache.set(error_cache_key, error_data, timeout=3600)  # 1 hour
                return None
                
            else:
                print(f"GitHub API error for {username}/{repo}: {response.status_code}")
                # Cache other errors for 30 minutes
                if self.cache:
                    error_data = {
                        'error': 'api_error',
                        'status_code': response.status_code,
                        'message': f'API error: {response.status_code}',
                        'cached_at': datetime.utcnow().isoformat()
                    }
                    self.cache.set(error_cache_key, error_data, timeout=1800)  # 30 minutes
                return None
                
        except requests.exceptions.Timeout:
            print(f"Timeout fetching GitHub data for {username}/{repo}")
            # Cache timeout errors for 15 minutes
            if self.cache:
                error_data = {
                    'error': 'timeout',
                    'message': 'Request timeout',
                    'cached_at': datetime.utcnow().isoformat()
                }
                self.cache.set(error_cache_key, error_data, timeout=900)  # 15 minutes
            return None
            
        except Exception as e:
            print(f"Error fetching GitHub data for {username}/{repo}: {e}")
            # Cache general errors for 15 minutes
            if self.cache:
                error_data = {
                    'error': 'general_error',
                    'message': str(e),
                    'cached_at': datetime.utcnow().isoformat()
                }
                self.cache.set(error_cache_key, error_data, timeout=900)  # 15 minutes
            return None
    
    def get_rate_limit_info(self):
        """Get current rate limit information"""
        try:
            response = requests.get(f"{self.base_url}/rate_limit", headers=self.headers, timeout=5)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching rate limit info: {e}")
        return None
    
    def clear_cache_for_repo(self, username, repo):
        """Clear cache for a specific repository"""
        if self.cache:
            cache_key = self._get_cache_key(username, repo)
            error_cache_key = self._get_error_cache_key(username, repo)
            self.cache.delete(cache_key)
            self.cache.delete(error_cache_key)
            print(f"Cleared cache for {username}/{repo}")
    
    def clear_all_cache(self):
        """Clear all GitHub cache"""
        if self.cache:
            self.cache.clear()
            print("Cleared all GitHub cache")
    
    def get_cache_stats(self):
        """Get cache statistics"""
        if not self.cache:
            return {'cache_enabled': False}
        
        # This is a basic implementation, Redis cache might have more detailed stats
        return {
            'cache_enabled': True,
            'cache_type': type(self.cache.cache).__name__ if hasattr(self.cache, 'cache') else 'Unknown'
        }

# Global instance
github_service = GitHubService()
