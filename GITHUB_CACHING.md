# GitHub API Caching System

This project implements a sophisticated caching system for GitHub API requests to improve performance and handle rate limits effectively.

## Features

### 🚀 Intelligent Caching
- **Redis Support**: Production-ready caching with Redis
- **Fallback Cache**: In-memory caching when Redis is unavailable
- **Error Caching**: Prevents repeated failed API calls
- **Configurable TTL**: Different cache durations for different scenarios

### ⚡ Performance Benefits
- **Faster Load Times**: Cached data loads instantly
- **Reduced API Calls**: Significant reduction in GitHub API usage
- **Rate Limit Protection**: Intelligent error caching prevents hitting rate limits
- **Background Updates**: Gradual updates without blocking user requests

### 🛡️ Error Handling
- **404 Handling**: Caches repository not found errors for 6 hours
- **Rate Limit Handling**: Caches rate limit errors for 1 hour
- **Timeout Handling**: Caches timeout errors for 15 minutes
- **General Error Handling**: Caches other errors for 15 minutes

## Configuration

### Environment Variables

```bash
# Optional: GitHub Personal Access Token (recommended)
GITHUB_TOKEN=your_personal_access_token

# Optional: Redis URL for production caching
REDIS_URL=redis://localhost:6379/0
```

### Cache Durations

| Data Type | Cache Duration | Reason |
|-----------|---------------|---------|
| Successful API Response | 2 hours | Balance between freshness and performance |
| 404 Not Found | 6 hours | Avoid repeated calls for non-existent repos |
| Rate Limit/403 | 1 hour | Respect GitHub's rate limiting |
| Timeout | 15 minutes | Quick retry for temporary network issues |
| General Errors | 15 minutes | Quick retry for other temporary issues |

## Usage

### CLI Commands

```bash
# Update GitHub data for all projects
flask update-github-data

# Force update (ignores cache and time checks)
flask update-github-data --force

# Update specific project
flask update-github-data --project-id 1

# Check cache statistics
flask github-cache-stats

# Clear all cache
flask clear-github-cache

# Clear cache for specific repository
flask clear-github-cache --repo username/repo-name
```

### API Endpoints

```bash
# Get cache statistics
GET /git/api/github/cache-stats

# Clear cache (admin)
POST /git/api/github/clear-cache
Content-Type: application/json
{"repo": "username/repo-name"}  # Optional: specific repo

# Force refresh project data
POST /git/api/github/force-refresh/1  # Project ID
```

## How It Works

### 1. Request Flow
```
User Request → Check Cache → API Call (if needed) → Update Database → Return Data
```

### 2. Background Updates
- Only 3 projects are updated per page request
- Prevents blocking user experience
- Gradual data synchronization

### 3. Cache Keys
- Repository data: `github_repo:username:repo`
- Error data: `github_error:username:repo`

### 4. Error Prevention
- Invalid repository formats are rejected early
- Failed repositories are cached to prevent repeated failures
- Rate limit information is monitored and respected

## Benefits

### Before Caching
- ❌ Every page load triggered multiple API calls
- ❌ 404 errors repeated on every request
- ❌ Slow page load times
- ❌ Risk of hitting GitHub rate limits
- ❌ Poor user experience during API failures

### After Caching
- ✅ Instant data loading from cache
- ✅ Failed repositories cached to prevent repeated errors
- ✅ Fast page load times
- ✅ Efficient API usage with rate limit protection
- ✅ Graceful handling of GitHub API issues
- ✅ Background data updates

## Monitoring

### Cache Statistics
The system provides detailed statistics including:
- Cache type (Redis/Simple)
- GitHub API rate limit status
- Cache hit/miss information (Redis only)

### Logging
All GitHub API operations are logged with:
- Success/failure status
- Repository information
- Error details
- Cache operations

## Production Recommendations

1. **Use Redis**: Set `REDIS_URL` environment variable
2. **GitHub Token**: Set `GITHUB_TOKEN` for higher rate limits
3. **Background Jobs**: Run `flask update-github-data` as a cron job
4. **Monitoring**: Check cache stats regularly
5. **Error Alerts**: Monitor application logs for repeated failures

## Troubleshooting

### Common Issues

**Issue**: Slow page loads
- **Solution**: Check if Redis is running and `REDIS_URL` is set correctly

**Issue**: GitHub rate limit errors
- **Solution**: Set `GITHUB_TOKEN` environment variable

**Issue**: Stale data
- **Solution**: Use `flask update-github-data --force` to refresh all data

**Issue**: Repeated 404 errors in logs
- **Solution**: This is normal - the system caches these to prevent repeated API calls

### Cache Debugging

```bash
# Check if caching is working
flask github-cache-stats

# Clear problematic cache entries
flask clear-github-cache --repo problematic/repo

# Force refresh all data
flask update-github-data --force
```
