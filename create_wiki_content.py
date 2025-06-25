#!/usr/bin/env python3
"""
Script to create wiki categories and articles for the portfolio website
"""

import sys
import os
sys.path.append('/home/ubuntu/portfolio')

from app import app
from database import db
from models import WikiCategory, WikiArticle
from datetime import datetime

def create_categories():
    """Create wiki categories"""
    categories_data = [
        {'name': 'Programming', 'description': 'General programming concepts and practices'},
        {'name': 'Web Development', 'description': 'Frontend and backend web development'},
        {'name': 'DevOps', 'description': 'Development operations and deployment'},
        {'name': 'Data Science', 'description': 'Data analysis and machine learning'},
        {'name': 'Tools', 'description': 'Development tools and utilities'},
        {'name': 'Security', 'description': 'Cybersecurity and web security'},
        {'name': 'Data Structure & Algorithms', 'description': 'Computer science fundamentals'},
        {'name': 'Python', 'description': 'Python programming language'},
        {'name': 'TypeScript', 'description': 'TypeScript programming language'},
        {'name': 'JavaScript', 'description': 'JavaScript programming language'},
        {'name': 'HTML5', 'description': 'HTML5 markup language'},
        {'name': 'CSS3', 'description': 'CSS3 styling language'},
        {'name': 'Go', 'description': 'Go programming language'},
    ]
    
    categories = {}
    created_count = 0
    
    for category_data in categories_data:
        # Check if category already exists
        existing = WikiCategory.query.filter_by(name=category_data['name']).first()
        if existing:
            categories[category_data['name']] = existing.id
            print(f"Category already exists: {category_data['name']}")
            continue
            
        # Create category
        category = WikiCategory(
            name=category_data['name'],
            description=category_data['description']
        )
        
        db.session.add(category)
        db.session.flush()  # Get the ID
        categories[category_data['name']] = category.id
        created_count += 1
        print(f"Created category: {category_data['name']}")
    
    db.session.commit()
    print(f"\nCreated {created_count} new categories")
    return categories

def create_articles(categories):
    """Create wiki categories"""
    articles_data = [
        # Your existing articles
        {
            'title': 'Python Best Practices',
            'content': '''# Python Best Practices: A Comprehensive Guide

## Table of Contents
1. [Code Style and Formatting](#code-style)
2. [Naming Conventions](#naming)
3. [Function and Class Design](#design)
4. [Error Handling](#error-handling)
5. [Performance Optimization](#performance)
6. [Testing Strategies](#testing)
7. [Documentation](#documentation)
8. [Security Considerations](#security)

## Code Style and Formatting {#code-style}

### PEP 8 Compliance
Python Enhancement Proposal 8 (PEP 8) is the style guide for Python code. Following PEP 8 ensures your code is readable and consistent with the broader Python community.

```python
# Good: Clear spacing and structure
def calculate_compound_interest(principal, rate, time, compound_frequency=1):
    """Calculate compound interest using the standard formula."""
    return principal * (1 + rate / compound_frequency) ** (compound_frequency * time)

# Bad: Poor spacing and structure
def calculate_compound_interest(principal,rate,time,compound_frequency=1):
    return principal*(1+rate/compound_frequency)**(compound_frequency*time)
```

### Line Length and Breaking
Keep lines under 79 characters for code and 72 for comments and docstrings:

```python
# Good: Proper line breaking
result = some_function_with_a_long_name(
    argument_one,
    argument_two,
    argument_three
)

# Good: Breaking long strings
message = (
    "This is a very long string that would exceed the line limit "
    "so we break it into multiple lines for better readability."
)
```

### Import Organization
Organize imports in the following order:
1. Standard library imports
2. Third-party library imports
3. Local application imports

```python
# Standard library
import os
import sys
from datetime import datetime

# Third-party
import requests
import numpy as np
from flask import Flask

# Local
from .models import User
from .utils import helper_function
```

## Naming Conventions {#naming}

### Variables and Functions
Use lowercase with underscores (snake_case):

```python
# Good
user_name = "john_doe"
total_amount = 1500.50

def get_user_profile(user_id):
    pass

def calculate_tax_amount(income, tax_rate):
    pass
```

### Classes
Use CapWords (PascalCase):

```python
class UserProfile:
    def __init__(self, username, email):
        self.username = username
        self.email = email

class DatabaseConnection:
    pass
```

### Constants
Use uppercase with underscores:

```python
MAX_RETRY_ATTEMPTS = 3
DEFAULT_TIMEOUT = 30
API_BASE_URL = "https://api.example.com"
```

### Private Members
Use leading underscore for internal use:

```python
class Calculator:
    def __init__(self):
        self._internal_state = {}
        self.__private_data = []  # Name mangling for true privacy
    
    def _helper_method(self):
        """Internal helper method."""
        pass
```

## Function and Class Design {#design}

### Single Responsibility Principle
Each function should do one thing well:

```python
# Good: Single responsibility
def validate_email(email):
    """Validate email format."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def send_email(to_address, subject, body):
    """Send email to specified address."""
    # Email sending logic here
    pass

# Bad: Multiple responsibilities
def validate_and_send_email(email, subject, body):
    """Validate email and send if valid."""
    # Validation logic
    # Email sending logic
    pass
```

### Function Parameters
Use clear parameter names and provide defaults where appropriate:

```python
def create_user_account(
    username,
    email,
    password,
    is_active=True,
    email_verified=False,
    created_by=None
):
    """Create a new user account with specified parameters."""
    pass

# Using keyword arguments for clarity
create_user_account(
    username="john_doe",
    email="john@example.com",
    password="secure_password",
    is_active=True
)
```

### Class Design Patterns

#### Builder Pattern
```python
class QueryBuilder:
    def __init__(self):
        self._query = ""
        self._conditions = []
        self._order_by = []
    
    def select(self, fields):
        self._query = f"SELECT {', '.join(fields)}"
        return self
    
    def from_table(self, table):
        self._query += f" FROM {table}"
        return self
    
    def where(self, condition):
        self._conditions.append(condition)
        return self
    
    def order_by(self, field, direction="ASC"):
        self._order_by.append(f"{field} {direction}")
        return self
    
    def build(self):
        query = self._query
        if self._conditions:
            query += " WHERE " + " AND ".join(self._conditions)
        if self._order_by:
            query += " ORDER BY " + ", ".join(self._order_by)
        return query

# Usage
query = (QueryBuilder()
         .select(["name", "email", "created_at"])
         .from_table("users")
         .where("is_active = 1")
         .where("email_verified = 1")
         .order_by("created_at", "DESC")
         .build())
```

## Error Handling {#error-handling}

### Specific Exception Handling
Catch specific exceptions rather than using bare except clauses:

```python
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException

def fetch_user_data(user_id):
    """Fetch user data from API with proper error handling."""
    try:
        response = requests.get(
            f"https://api.example.com/users/{user_id}",
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    
    except ConnectionError:
        logger.error("Failed to connect to the API")
        raise UserDataError("Unable to connect to user service")
    
    except Timeout:
        logger.error("API request timed out")
        raise UserDataError("Request timed out")
    
    except RequestException as e:
        logger.error(f"API request failed: {e}")
        raise UserDataError(f"Failed to fetch user data: {e}")
```

### Custom Exceptions
Create custom exception classes for your application:

```python
class UserDataError(Exception):
    """Raised when user data operations fail."""
    pass

class ValidationError(Exception):
    """Raised when data validation fails."""
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f"Validation error in {field}: {message}")

class ConfigurationError(Exception):
    """Raised when configuration is invalid."""
    pass
```

### Context Managers
Use context managers for resource management:

```python
import sqlite3
from contextlib import contextmanager

@contextmanager
def database_connection(db_path):
    """Context manager for database connections."""
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

# Usage
with database_connection("app.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
```

## Performance Optimization {#performance}

### List Comprehensions vs Loops
Use list comprehensions for simple transformations:

```python
# Good: List comprehension
squared_numbers = [x**2 for x in range(1000) if x % 2 == 0]

# Good: Generator expression for memory efficiency
squared_numbers = (x**2 for x in range(1000) if x % 2 == 0)

# Avoid: Traditional loop for simple operations
squared_numbers = []
for x in range(1000):
    if x % 2 == 0:
        squared_numbers.append(x**2)
```

### Dictionary and Set Operations
Leverage O(1) lookup times:

```python
# Good: Using sets for membership testing
valid_statuses = {"active", "pending", "suspended"}
if user_status in valid_statuses:
    process_user()

# Good: Dictionary for mapping
status_messages = {
    "active": "User is active",
    "pending": "User activation pending",
    "suspended": "User account suspended"
}
message = status_messages.get(user_status, "Unknown status")
```

### String Operations
Use join() for string concatenation:

```python
# Good: Using join
parts = ["Hello", "world", "from", "Python"]
message = " ".join(parts)

# Good: f-strings for formatting
name = "Alice"
age = 30
greeting = f"Hello, {name}! You are {age} years old."

# Avoid: String concatenation in loops
message = ""
for part in parts:
    message += part + " "
```

### Caching and Memoization
Use functools.lru_cache for expensive computations:

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    """Calculate Fibonacci number with memoization."""
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

@lru_cache(maxsize=None)
def expensive_calculation(param1, param2):
    """Expensive calculation that benefits from caching."""
    # Complex computation here
    result = param1 ** param2 + complex_algorithm(param1, param2)
    return result
```

## Testing Strategies {#testing}

### Unit Testing with pytest
Write comprehensive unit tests:

```python
import pytest
from myapp.calculator import Calculator
from myapp.exceptions import DivisionByZeroError

class TestCalculator:
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.calculator = Calculator()
    
    def test_addition(self):
        """Test basic addition functionality."""
        assert self.calculator.add(2, 3) == 5
        assert self.calculator.add(-1, 1) == 0
        assert self.calculator.add(0, 0) == 0
    
    def test_division_by_zero(self):
        """Test that division by zero raises appropriate exception."""
        with pytest.raises(DivisionByZeroError):
            self.calculator.divide(10, 0)
    
    @pytest.mark.parametrize("a,b,expected", [
        (2, 3, 6),
        (-2, 3, -6),
        (0, 5, 0),
        (2.5, 4, 10.0)
    ])
    def test_multiplication(self, a, b, expected):
        """Test multiplication with various inputs."""
        assert self.calculator.multiply(a, b) == expected
```

### Mocking External Dependencies
Use unittest.mock for testing:

```python
from unittest.mock import Mock, patch
import requests

def get_weather_data(city):
    """Fetch weather data from external API."""
    response = requests.get(f"http://api.weather.com/{city}")
    return response.json()

class TestWeatherService:
    @patch('requests.get')
    def test_get_weather_data(self, mock_get):
        """Test weather data fetching with mocked API."""
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "temperature": 25,
            "condition": "sunny"
        }
        mock_get.return_value = mock_response
        
        # Test the function
        result = get_weather_data("London")
        
        # Assertions
        assert result["temperature"] == 25
        assert result["condition"] == "sunny"
        mock_get.assert_called_once_with("http://api.weather.com/London")
```

## Documentation {#documentation}

### Docstring Conventions
Follow Google or NumPy style docstrings:

```python
def calculate_compound_interest(principal, rate, time, compound_frequency=1):
    """Calculate compound interest using the standard formula.
    
    Args:
        principal (float): The initial amount of money.
        rate (float): The annual interest rate (as a decimal).
        time (float): The number of years.
        compound_frequency (int, optional): Number of times interest is 
            compounded per year. Defaults to 1.
    
    Returns:
        float: The final amount after compound interest.
    
    Raises:
        ValueError: If any of the numeric parameters are negative.
        TypeError: If parameters are not numeric types.
    
    Example:
        >>> calculate_compound_interest(1000, 0.05, 10, 12)
        1643.62
    """
    if principal < 0 or rate < 0 or time < 0:
        raise ValueError("All parameters must be non-negative")
    
    return principal * (1 + rate / compound_frequency) ** (compound_frequency * time)
```

### Type Hints
Use type hints for better code documentation and IDE support:

```python
from typing import List, Dict, Optional, Union, Callable
from dataclasses import dataclass

@dataclass
class User:
    """User data class with type annotations."""
    id: int
    username: str
    email: str
    is_active: bool = True
    metadata: Optional[Dict[str, str]] = None

def process_users(
    users: List[User],
    filter_func: Callable[[User], bool],
    active_only: bool = True
) -> List[Dict[str, Union[str, int, bool]]]:
    """Process a list of users with optional filtering.
    
    Args:
        users: List of User objects to process.
        filter_func: Function to filter users.
        active_only: Whether to include only active users.
    
    Returns:
        List of user dictionaries.
    """
    filtered_users = [
        user for user in users 
        if (not active_only or user.is_active) and filter_func(user)
    ]
    
    return [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active
        }
        for user in filtered_users
    ]
```

## Security Considerations {#security}

### Input Validation and Sanitization
Always validate and sanitize user input:

```python
import re
from html import escape

def validate_username(username: str) -> bool:
    """Validate username format and length."""
    if not isinstance(username, str):
        return False
    
    if len(username) < 3 or len(username) > 30:
        return False
    
    # Allow only alphanumeric characters and underscores
    pattern = r'^[a-zA-Z0-9_]+$'
    return bool(re.match(pattern, username))

def sanitize_html_input(user_input: str) -> str:
    """Sanitize HTML input to prevent XSS attacks."""
    return escape(user_input.strip())

def validate_email_format(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
```

### Password Security
Implement secure password handling:

```python
import hashlib
import secrets
from cryptography.fernet import Fernet

def generate_salt() -> bytes:
    """Generate a random salt for password hashing."""
    return secrets.token_bytes(32)

def hash_password(password: str, salt: bytes) -> bytes:
    """Hash password with salt using PBKDF2."""
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)

def verify_password(password: str, salt: bytes, hashed: bytes) -> bool:
    """Verify password against stored hash."""
    return hash_password(password, salt) == hashed

class SecureStorage:
    """Secure storage for sensitive data."""
    
    def __init__(self, key: bytes = None):
        self.key = key or Fernet.generate_key()
        self.cipher = Fernet(self.key)
    
    def encrypt(self, data: str) -> bytes:
        """Encrypt sensitive data."""
        return self.cipher.encrypt(data.encode())
    
    def decrypt(self, encrypted_data: bytes) -> str:
        """Decrypt sensitive data."""
        return self.cipher.decrypt(encrypted_data).decode()
```

### Environment Variables for Secrets
Never hardcode secrets in your code:

```python
import os
from typing import Optional

def get_database_url() -> str:
    """Get database URL from environment variables."""
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        raise ValueError("DATABASE_URL environment variable is required")
    return db_url

def get_api_key(service_name: str) -> str:
    """Get API key for specified service."""
    key = os.getenv(f'{service_name.upper()}_API_KEY')
    if not key:
        raise ValueError(f"{service_name} API key not found in environment")
    return key

# Configuration class
class Config:
    """Application configuration from environment variables."""
    
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SECRET_KEY = os.getenv('SECRET_KEY') or secrets.token_hex(32)
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    API_RATE_LIMIT = int(os.getenv('API_RATE_LIMIT', '1000'))
```

This comprehensive guide covers the essential Python best practices that every developer should follow. By implementing these practices, you'll write more maintainable, secure, and efficient Python code that follows industry standards and community conventions.

Remember that best practices evolve with the language and community. Stay updated with the latest Python Enhancement Proposals (PEPs) and continue learning from the Python community to keep your skills sharp and your code exemplary.''',
            'category': 'Programming',
            'tags': 'python,best-practices,coding-standards',
        },
        {
            'title': 'React Component Patterns',
            'content': '''# React Component Patterns: Modern Development Guide

## Table of Contents
1. [Introduction to React Components](#introduction)
2. [Functional vs Class Components](#functional-vs-class)
3. [Component Composition Patterns](#composition)
4. [State Management Patterns](#state-management)
5. [Higher-Order Components (HOCs)](#hocs)
6. [Render Props Pattern](#render-props)
7. [Custom Hooks](#custom-hooks)
8. [Context and Provider Patterns](#context)
9. [Performance Optimization Patterns](#performance)
10. [Testing Patterns](#testing)

## Introduction to React Components {#introduction}

React components are the building blocks of React applications. They encapsulate UI logic and state, promoting reusability and maintainability. Understanding component patterns is crucial for building scalable React applications.

### Component Fundamentals
```jsx
// Basic functional component
function Welcome({ name, age }) {
  return (
    <div className="welcome">
      <h1>Hello, {name}!</h1>
      <p>You are {age} years old.</p>
    </div>
  );
}

// Component with default props
Welcome.defaultProps = {
  name: 'Guest',
  age: 0
};

// Usage
<Welcome name="Alice" age={25} />
```

### Component Types by Purpose
1. **Presentational Components**: Focus on UI rendering
2. **Container Components**: Handle business logic and state
3. **Layout Components**: Structure and positioning
4. **Utility Components**: Shared functionality

## Functional vs Class Components {#functional-vs-class}

### Modern Functional Components with Hooks
```jsx
import React, { useState, useEffect, useCallback, useMemo } from 'react';

function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Effect for data fetching
  useEffect(() => {
    let cancelled = false;
    
    async function fetchUser() {
      try {
        setLoading(true);
        const response = await fetch(`/api/users/${userId}`);
        const userData = await response.json();
        
        if (!cancelled) {
          setUser(userData);
          setError(null);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err.message);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    fetchUser();

    return () => {
      cancelled = true;
    };
  }, [userId]);

  // Memoized computed value
  const userDisplayName = useMemo(() => {
    if (!user) return '';
    return `${user.firstName} ${user.lastName}`.trim();
  }, [user]);

  // Memoized event handler
  const handleRefresh = useCallback(() => {
    setUser(null);
    setLoading(true);
    setError(null);
  }, []);

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} onRetry={handleRefresh} />;
  if (!user) return <div>User not found</div>;

  return (
    <div className="user-profile">
      <Avatar src={user.avatar} alt={userDisplayName} />
      <h2>{userDisplayName}</h2>
      <p>{user.email}</p>
      <button onClick={handleRefresh}>Refresh</button>
    </div>
  );
}
```

### Legacy Class Components (for reference)
```jsx
class UserProfileClass extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      user: null,
      loading: true,
      error: null
    };
    this.handleRefresh = this.handleRefresh.bind(this);
  }

  async componentDidMount() {
    await this.fetchUser();
  }

  async componentDidUpdate(prevProps) {
    if (prevProps.userId !== this.props.userId) {
      await this.fetchUser();
    }
  }

  async fetchUser() {
    try {
      this.setState({ loading: true });
      const response = await fetch(`/api/users/${this.props.userId}`);
      const user = await response.json();
      this.setState({ user, error: null });
    } catch (error) {
      this.setState({ error: error.message });
    } finally {
      this.setState({ loading: false });
    }
  }

  handleRefresh() {
    this.setState({ user: null, loading: true, error: null });
    this.fetchUser();
  }

  render() {
    const { user, loading, error } = this.state;
    
    if (loading) return <LoadingSpinner />;
    if (error) return <ErrorMessage message={error} onRetry={this.handleRefresh} />;
    if (!user) return <div>User not found</div>;

    return (
      <div className="user-profile">
        <Avatar src={user.avatar} alt={`${user.firstName} ${user.lastName}`} />
        <h2>{user.firstName} {user.lastName}</h2>
        <p>{user.email}</p>
        <button onClick={this.handleRefresh}>Refresh</button>
      </div>
    );
  }
}
```

## Component Composition Patterns {#composition}

### Children Pattern
```jsx
function Card({ children, title, className = '' }) {
  return (
    <div className={`card ${className}`}>
      {title && <div className="card-header">{title}</div>}
      <div className="card-body">
        {children}
      </div>
    </div>
  );
}

// Usage
<Card title="User Information">
  <UserProfile userId={123} />
  <UserActions userId={123} />
</Card>
```

### Compound Components Pattern
```jsx
function Tabs({ children, defaultTab = 0 }) {
  const [activeTab, setActiveTab] = useState(defaultTab);
  const tabs = React.Children.toArray(children);

  return (
    <div className="tabs">
      <div className="tab-list">
        {tabs.map((tab, index) => (
          <button
            key={index}
            className={`tab ${index === activeTab ? 'active' : ''}`}
            onClick={() => setActiveTab(index)}
          >
            {tab.props.label}
          </button>
        ))}
      </div>
      <div className="tab-content">
        {tabs[activeTab]}
      </div>
    </div>
  );
}

function TabPane({ children, label }) {
  return <div className="tab-pane">{children}</div>;
}

// Usage
<Tabs defaultTab={1}>
  <TabPane label="Profile">
    <UserProfile />
  </TabPane>
  <TabPane label="Settings">
    <UserSettings />
  </TabPane>
  <TabPane label="Activity">
    <UserActivity />
  </TabPane>
</Tabs>
```

### Slot Pattern
```jsx
function Layout({ header, sidebar, main, footer }) {
  return (
    <div className="layout">
      <header className="layout-header">{header}</header>
      <div className="layout-body">
        <aside className="layout-sidebar">{sidebar}</aside>
        <main className="layout-main">{main}</main>
      </div>
      <footer className="layout-footer">{footer}</footer>
    </div>
  );
}

// Usage
<Layout
  header={<Navigation />}
  sidebar={<SidebarMenu />}
  main={<MainContent />}
  footer={<Footer />}
/>
```

## State Management Patterns {#state-management}

### Local State with useState
```jsx
function Counter({ initialValue = 0, step = 1 }) {
  const [count, setCount] = useState(initialValue);

  const increment = useCallback(() => {
    setCount(prevCount => prevCount + step);
  }, [step]);

  const decrement = useCallback(() => {
    setCount(prevCount => prevCount - step);
  }, [step]);

  const reset = useCallback(() => {
    setCount(initialValue);
  }, [initialValue]);

  return (
    <div className="counter">
      <span className="count">{count}</span>
      <div className="controls">
        <button onClick={decrement}>-</button>
        <button onClick={reset}>Reset</button>
        <button onClick={increment}>+</button>
      </div>
    </div>
  );
}
```

### State with useReducer
```jsx
function formReducer(state, action) {
  switch (action.type) {
    case 'SET_FIELD':
      return {
        ...state,
        values: {
          ...state.values,
          [action.field]: action.value
        },
        errors: {
          ...state.errors,
          [action.field]: null
        }
      };
    
    case 'SET_ERROR':
      return {
        ...state,
        errors: {
          ...state.errors,
          [action.field]: action.error
        }
      };
    
    case 'SET_LOADING':
      return {
        ...state,
        loading: action.loading
      };
    
    case 'RESET_FORM':
      return {
        values: action.initialValues || {},
        errors: {},
        loading: false
      };
    
    default:
      return state;
  }
}

function ContactForm({ onSubmit, initialValues = {} }) {
  const [state, dispatch] = useReducer(formReducer, {
    values: initialValues,
    errors: {},
    loading: false
  });

  const setField = useCallback((field, value) => {
    dispatch({ type: 'SET_FIELD', field, value });
  }, []);

  const setError = useCallback((field, error) => {
    dispatch({ type: 'SET_ERROR', field, error });
  }, []);

  const validateField = useCallback((field, value) => {
    switch (field) {
      case 'email':
        if (!value.includes('@')) {
          setError(field, 'Invalid email address');
          return false;
        }
        break;
      case 'name':
        if (value.length < 2) {
          setError(field, 'Name must be at least 2 characters');
          return false;
        }
        break;
      default:
        break;
    }
    return true;
  }, [setError]);

  const handleSubmit = useCallback(async (e) => {
    e.preventDefault();
    
    // Validate all fields
    const isValid = Object.keys(state.values).every(field =>
      validateField(field, state.values[field])
    );

    if (!isValid) return;

    dispatch({ type: 'SET_LOADING', loading: true });
    
    try {
      await onSubmit(state.values);
      dispatch({ type: 'RESET_FORM', initialValues });
    } catch (error) {
      setError('general', error.message);
    } finally {
      dispatch({ type: 'SET_LOADING', loading: false });
    }
  }, [state.values, validateField, onSubmit, initialValues, setError]);

  return (
    <form onSubmit={handleSubmit} className="contact-form">
      <div className="form-group">
        <label htmlFor="name">Name</label>
        <input
          id="name"
          type="text"
          value={state.values.name || ''}
          onChange={(e) => setField('name', e.target.value)}
          onBlur={(e) => validateField('name', e.target.value)}
        />
        {state.errors.name && <span className="error">{state.errors.name}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          value={state.values.email || ''}
          onChange={(e) => setField('email', e.target.value)}
          onBlur={(e) => validateField('email', e.target.value)}
        />
        {state.errors.email && <span className="error">{state.errors.email}</span>}
      </div>

      {state.errors.general && (
        <div className="error general-error">{state.errors.general}</div>
      )}

      <button type="submit" disabled={state.loading}>
        {state.loading ? 'Submitting...' : 'Submit'}
      </button>
    </form>
  );
}
```

## Higher-Order Components (HOCs) {#hocs}

### Authentication HOC
```jsx
function withAuth(WrappedComponent, requiredRole = null) {
  function AuthenticatedComponent(props) {
    const { user, loading } = useAuth();

    if (loading) {
      return <LoadingSpinner />;
    }

    if (!user) {
      return <LoginPrompt />;
    }

    if (requiredRole && !user.roles.includes(requiredRole)) {
      return <AccessDenied />;
    }

    return <WrappedComponent {...props} user={user} />;
  }

  AuthenticatedComponent.displayName = `withAuth(${WrappedComponent.displayName || WrappedComponent.name})`;
  
  return AuthenticatedComponent;
}

// Usage
const ProtectedDashboard = withAuth(Dashboard, 'admin');
const UserProfile = withAuth(Profile);
```

### Loading HOC
```jsx
function withLoading(WrappedComponent) {
  function LoadingComponent({ isLoading, loadingMessage = 'Loading...', ...props }) {
    if (isLoading) {
      return (
        <div className="loading-container">
          <LoadingSpinner />
          <p>{loadingMessage}</p>
        </div>
      );
    }

    return <WrappedComponent {...props} />;
  }

  LoadingComponent.displayName = `withLoading(${WrappedComponent.displayName || WrappedComponent.name})`;
  
  return LoadingComponent;
}

// Usage
const UserListWithLoading = withLoading(UserList);

<UserListWithLoading 
  isLoading={loading} 
  loadingMessage="Fetching users..." 
  users={users} 
/>
```

## Render Props Pattern {#render-props}

### Data Fetcher Component
```jsx
function DataFetcher({ url, children, render }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;

    async function fetchData() {
      try {
        setLoading(true);
        const response = await fetch(url);
        const result = await response.json();
        
        if (!cancelled) {
          setData(result);
          setError(null);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err.message);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    fetchData();

    return () => {
      cancelled = true;
    };
  }, [url]);

  const renderProps = { data, loading, error };

  // Support both render prop and children function
  if (render) {
    return render(renderProps);
  }

  if (typeof children === 'function') {
    return children(renderProps);
  }

  return null;
}

// Usage with render prop
<DataFetcher 
  url="/api/users" 
  render={({ data, loading, error }) => {
    if (loading) return <LoadingSpinner />;
    if (error) return <ErrorMessage message={error} />;
    return <UserList users={data} />;
  }} 
/>

// Usage with children function
<DataFetcher url="/api/posts">
  {({ data, loading, error }) => {
    if (loading) return <LoadingSpinner />;
    if (error) return <ErrorMessage message={error} />;
    return <PostList posts={data} />;
  }}
</DataFetcher>
```

### Form Validation Render Prop
```jsx
function FormValidator({ validationRules, children }) {
  const [values, setValues] = useState({});
  const [errors, setErrors] = useState({});

  const validate = useCallback((field, value) => {
    const rule = validationRules[field];
    if (!rule) return true;

    const error = rule(value, values);
    setErrors(prev => ({ ...prev, [field]: error }));
    return !error;
  }, [validationRules, values]);

  const setValue = useCallback((field, value) => {
    setValues(prev => ({ ...prev, [field]: value }));
    validate(field, value);
  }, [validate]);

  const validateAll = useCallback(() => {
    const newErrors = {};
    let isValid = true;

    Object.keys(validationRules).forEach(field => {
      const error = validationRules[field](values[field], values);
      if (error) {
        newErrors[field] = error;
        isValid = false;
      }
    });

    setErrors(newErrors);
    return isValid;
  }, [validationRules, values]);

  return children({
    values,
    errors,
    setValue,
    validate,
    validateAll,
    isValid: Object.keys(errors).length === 0
  });
}

// Usage
const validationRules = {
  email: (value) => {
    if (!value) return 'Email is required';
    if (!value.includes('@')) return 'Invalid email format';
    return null;
  },
  password: (value) => {
    if (!value) return 'Password is required';
    if (value.length < 8) return 'Password must be at least 8 characters';
    return null;
  }
};

<FormValidator validationRules={validationRules}>
  {({ values, errors, setValue, validateAll, isValid }) => (
    <form onSubmit={(e) => {
      e.preventDefault();
      if (validateAll()) {
        onSubmit(values);
      }
    }}>
      <input
        type="email"
        value={values.email || ''}
        onChange={(e) => setValue('email', e.target.value)}
        placeholder="Email"
      />
      {errors.email && <span className="error">{errors.email}</span>}
      
      <input
        type="password"
        value={values.password || ''}
        onChange={(e) => setValue('password', e.target.value)}
        placeholder="Password"
      />
      {errors.password && <span className="error">{errors.password}</span>}
      
      <button type="submit" disabled={!isValid}>Submit</button>
    </form>
  )}
</FormValidator>
```

## Custom Hooks {#custom-hooks}

### useLocalStorage Hook
```jsx
function useLocalStorage(key, initialValue) {
  // Get value from localStorage or use initial value
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(`Error reading localStorage key "${key}":`, error);
      return initialValue;
    }
  });

  // Return a wrapped version of useState's setter function that persists the new value to localStorage
  const setValue = useCallback((value) => {
    try {
      // Allow value to be a function so we have the same API as useState
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(`Error setting localStorage key "${key}":`, error);
    }
  }, [key, storedValue]);

  return [storedValue, setValue];
}

// Usage
function UserPreferences() {
  const [theme, setTheme] = useLocalStorage('theme', 'light');
  const [language, setLanguage] = useLocalStorage('language', 'en');

  return (
    <div>
      <select value={theme} onChange={(e) => setTheme(e.target.value)}>
        <option value="light">Light</option>
        <option value="dark">Dark</option>
      </select>
      
      <select value={language} onChange={(e) => setLanguage(e.target.value)}>
        <option value="en">English</option>
        <option value="es">Spanish</option>
        <option value="fr">French</option>
      </select>
    </div>
  );
}
```

### useDebounce Hook
```jsx
function useDebounce(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}

// Usage in search component
function SearchComponent() {
  const [searchTerm, setSearchTerm] = useState('');
  const debouncedSearchTerm = useDebounce(searchTerm, 300);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (debouncedSearchTerm) {
      setLoading(true);
      searchAPI(debouncedSearchTerm).then(results => {
        setResults(results);
        setLoading(false);
      });
    } else {
      setResults([]);
    }
  }, [debouncedSearchTerm]);

  return (
    <div>
      <input
        type="text"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        placeholder="Search..."
      />
      {loading && <div>Searching...</div>}
      <SearchResults results={results} />
    </div>
  );
}
```

### useApi Hook
```jsx
function useApi(url, options = {}) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        },
        ...options
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [url, options]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const refetch = useCallback(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch };
}

// Usage
function UserProfile({ userId }) {
  const { data: user, loading, error, refetch } = useApi(`/api/users/${userId}`);

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} onRetry={refetch} />;
  if (!user) return <div>User not found</div>;

  return (
    <div className="user-profile">
      <h2>{user.name}</h2>
      <p>{user.email}</p>
      <button onClick={refetch}>Refresh</button>
    </div>
  );
}
```

## Context and Provider Patterns {#context}

### Theme Context
```jsx
const ThemeContext = createContext();

function ThemeProvider({ children }) {
  const [theme, setTheme] = useLocalStorage('theme', 'light');

  const toggleTheme = useCallback(() => {
    setTheme(prevTheme => prevTheme === 'light' ? 'dark' : 'light');
  }, [setTheme]);

  const value = useMemo(() => ({
    theme,
    toggleTheme,
    isDark: theme === 'dark'
  }), [theme, toggleTheme]);

  return (
    <ThemeContext.Provider value={value}>
      <div className={`app-theme-${theme}`}>
        {children}
      </div>
    </ThemeContext.Provider>
  );
}

function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}

// Usage
function App() {
  return (
    <ThemeProvider>
      <Header />
      <Main />
      <Footer />
    </ThemeProvider>
  );
}

function Header() {
  const { theme, toggleTheme } = useTheme();
  
  return (
    <header>
      <h1>My App</h1>
      <button onClick={toggleTheme}>
        Switch to {theme === 'light' ? 'dark' : 'light'} mode
      </button>
    </header>
  );
}
```

### Authentication Context
```jsx
const AuthContext = createContext();

function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for existing session
    const token = localStorage.getItem('authToken');
    if (token) {
      fetchUserProfile(token).then(user => {
        setUser(user);
        setLoading(false);
      }).catch(() => {
        localStorage.removeItem('authToken');
        setLoading(false);
      });
    } else {
      setLoading(false);
    }
  }, []);

  const login = useCallback(async (email, password) => {
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      const data = await response.json();
      
      if (response.ok) {
        localStorage.setItem('authToken', data.token);
        setUser(data.user);
        return { success: true };
      } else {
        return { success: false, error: data.message };
      }
    } catch (error) {
      return { success: false, error: error.message };
    }
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem('authToken');
    setUser(null);
  }, []);

  const value = useMemo(() => ({
    user,
    login,
    logout,
    isAuthenticated: !!user,
    loading
  }), [user, login, logout, loading]);

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
```

## Performance Optimization Patterns {#performance}

### Memoization with React.memo
```jsx
const UserCard = React.memo(function UserCard({ user, onSelect }) {
  return (
    <div className="user-card" onClick={() => onSelect(user.id)}>
      <img src={user.avatar} alt={user.name} />
      <h3>{user.name}</h3>
      <p>{user.email}</p>
    </div>
  );
}, (prevProps, nextProps) => {
  // Custom comparison function
  return (
    prevProps.user.id === nextProps.user.id &&
    prevProps.user.name === nextProps.user.name &&
    prevProps.user.email === nextProps.user.email &&
    prevProps.user.avatar === nextProps.user.avatar &&
    prevProps.onSelect === nextProps.onSelect
  );
});

function UserList({ users }) {
  const [selectedUser, setSelectedUser] = useState(null);

  // Memoize the callback to prevent unnecessary re-renders
  const handleUserSelect = useCallback((userId) => {
    setSelectedUser(userId);
  }, []);

  return (
    <div className="user-list">
      {users.map(user => (
        <UserCard
          key={user.id}
          user={user}
          onSelect={handleUserSelect}
        />
      ))}
    </div>
  );
}
```

### Virtual Scrolling
```jsx
function VirtualList({ items, itemHeight, containerHeight, renderItem }) {
  const [scrollTop, setScrollTop] = useState(0);
  
  const visibleStart = Math.floor(scrollTop / itemHeight);
  const visibleEnd = Math.min(
    visibleStart + Math.ceil(containerHeight / itemHeight) + 1,
    items.length
  );

  const visibleItems = items.slice(visibleStart, visibleEnd);
  const totalHeight = items.length * itemHeight;
  const offsetY = visibleStart * itemHeight;

  const handleScroll = useCallback((e) => {
    setScrollTop(e.target.scrollTop);
  }, []);

  return (
    <div
      style={{ height: containerHeight, overflow: 'auto' }}
      onScroll={handleScroll}
    >
      <div style={{ height: totalHeight, position: 'relative' }}>
        <div style={{ transform: `translateY(${offsetY}px)` }}>
          {visibleItems.map((item, index) => (
            <div
              key={visibleStart + index}
              style={{ height: itemHeight }}
            >
              {renderItem(item, visibleStart + index)}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// Usage
function App() {
  const items = Array.from({ length: 10000 }, (_, i) => ({ id: i, name: `Item ${i}` }));

  return (
    <VirtualList
      items={items}
      itemHeight={50}
      containerHeight={400}
      renderItem={(item) => (
        <div className="list-item">
          {item.name}
        </div>
      )}
    />
  );
}
```

## Testing Patterns {#testing}

### Component Testing with React Testing Library
```jsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { UserProfile } from './UserProfile';

// Mock API calls
jest.mock('../api/userApi', () => ({
  fetchUser: jest.fn(),
  updateUser: jest.fn()
}));

describe('UserProfile', () => {
  const mockUser = {
    id: 1,
    name: 'John Doe',
    email: 'john@example.com',
    avatar: 'avatar.jpg'
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('displays user information correctly', async () => {
    fetchUser.mockResolvedValue(mockUser);

    render(<UserProfile userId={1} />);

    // Check loading state
    expect(screen.getByText('Loading...')).toBeInTheDocument();

    // Wait for user data to load
    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument();
    });

    expect(screen.getByText('john@example.com')).toBeInTheDocument();
    expect(screen.getByAltText('John Doe')).toHaveAttribute('src', 'avatar.jpg');
  });

  test('handles edit mode correctly', async () => {
    fetchUser.mockResolvedValue(mockUser);
    updateUser.mockResolvedValue({ ...mockUser, name: 'Jane Doe' });

    render(<UserProfile userId={1} />);

    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument();
    });

    // Enter edit mode
    fireEvent.click(screen.getByText('Edit'));

    // Check if form is displayed
    expect(screen.getByDisplayValue('John Doe')).toBeInTheDocument();
    expect(screen.getByDisplayValue('john@example.com')).toBeInTheDocument();

    // Update name
    const nameInput = screen.getByDisplayValue('John Doe');
    await userEvent.clear(nameInput);
    await userEvent.type(nameInput, 'Jane Doe');

    // Save changes
    fireEvent.click(screen.getByText('Save'));

    // Verify API call
    await waitFor(() => {
      expect(updateUser).toHaveBeenCalledWith(1, {
        ...mockUser,
        name: 'Jane Doe'
      });
    });
  });

  test('displays error message on fetch failure', async () => {
    fetchUser.mockRejectedValue(new Error('Network error'));

    render(<UserProfile userId={1} />);

    await waitFor(() => {
      expect(screen.getByText('Error loading user data')).toBeInTheDocument();
    });

    // Test retry functionality
    fireEvent.click(screen.getByText('Retry'));
    expect(fetchUser).toHaveBeenCalledTimes(2);
  });
});
```

### Custom Hook Testing
```jsx
import { renderHook, act } from '@testing-library/react';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  test('initializes with default value', () => {
    const { result } = renderHook(() => useCounter());
    
    expect(result.current.count).toBe(0);
  });

  test('initializes with custom value', () => {
    const { result } = renderHook(() => useCounter(10));
    
    expect(result.current.count).toBe(10);
  });

  test('increments count', () => {
    const { result } = renderHook(() => useCounter());
    
    act(() => {
      result.current.increment();
    });
    
    expect(result.current.count).toBe(1);
  });

  test('decrements count', () => {
    const { result } = renderHook(() => useCounter(5));
    
    act(() => {
      result.current.decrement();
    });
    
    expect(result.current.count).toBe(4);
  });

  test('resets count', () => {
    const { result } = renderHook(() => useCounter(10));
    
    act(() => {
      result.current.increment();
      result.current.increment();
    });
    
    expect(result.current.count).toBe(12);
    
    act(() => {
      result.current.reset();
    });
    
    expect(result.current.count).toBe(10);
  });
});
```

This comprehensive guide covers the most important React component patterns used in modern React development. Understanding and applying these patterns will help you build more maintainable, performant, and testable React applications.

Each pattern serves a specific purpose and can be combined with others to create robust component architectures. The key is to choose the right pattern for your specific use case and maintain consistency throughout your application.''',
            'category': 'Web Development',
            'tags': 'react,javascript,frontend,components',
        },
        {
            'title': 'Docker Fundamentals',
            'content': '''# Docker Fundamentals: Complete Container Guide

## Table of Contents
1. [Introduction to Docker](#introduction)
2. [Docker Architecture](#architecture)
3. [Images and Containers](#images-containers)
4. [Dockerfile Best Practices](#dockerfile)
5. [Docker Networking](#networking)
6. [Volume Management](#volumes)
7. [Docker Compose](#compose)
8. [Security Considerations](#security)
9. [Performance Optimization](#performance)
10. [Production Deployment](#production)

## Introduction to Docker {#introduction}

Docker is a containerization platform that enables developers to package applications and their dependencies into lightweight, portable containers. These containers can run consistently across different environments, from development to production.

### Why Docker?
- **Consistency**: "It works on my machine" problems eliminated
- **Isolation**: Applications run in isolated environments
- **Portability**: Containers run anywhere Docker is installed
- **Scalability**: Easy horizontal scaling of applications
- **Resource Efficiency**: Containers share OS kernel, using fewer resources than VMs

### Key Concepts
```bash
# Container: Running instance of an image
docker run hello-world

# Image: Read-only template for creating containers
docker images

# Registry: Repository for storing and distributing images
docker push myapp:latest

# Volume: Persistent data storage
docker volume create mydata
```

## Docker Architecture {#architecture}

### Docker Engine Components
1. **Docker Daemon**: Background service managing containers
2. **Docker CLI**: Command-line interface for user interaction
3. **REST API**: Interface between CLI and daemon
4. **containerd**: High-level container runtime
5. **runc**: Low-level container runtime

### Container vs VM Architecture
```
Traditional VMs:
┌─────────────────┐ ┌─────────────────┐
│   Application   │ │   Application   │
├─────────────────┤ ├─────────────────┤
│   Guest OS      │ │   Guest OS      │
├─────────────────┤ ├─────────────────┤
│   Hypervisor    │ │   Hypervisor    │
├─────────────────┴─┴─────────────────┤
│           Host OS                   │
└─────────────────────────────────────┘

Docker Containers:
┌─────────────────┐ ┌─────────────────┐
│   Application   │ │   Application   │
├─────────────────┤ ├─────────────────┤
│   Docker Engine │ │   Docker Engine │
├─────────────────┴─┴─────────────────┤
│           Host OS                   │
└─────────────────────────────────────┘
```

### Container Lifecycle
```bash
# Create container (without starting)
docker create --name myapp nginx:alpine

# Start existing container
docker start myapp

# Run (create and start in one command)
docker run -d --name webapp nginx:alpine

# Stop container
docker stop webapp

# Restart container
docker restart webapp

# Remove container
docker rm webapp

# Force remove running container
docker rm -f webapp
```

## Images and Containers {#images-containers}

### Working with Images
```bash
# Pull image from registry
docker pull nginx:1.21-alpine

# List local images
docker images

# Inspect image details
docker inspect nginx:1.21-alpine

# View image history
docker history nginx:1.21-alpine

# Remove image
docker rmi nginx:1.21-alpine

# Build image from Dockerfile
docker build -t myapp:v1.0 .

# Tag image
docker tag myapp:v1.0 myregistry.com/myapp:v1.0

# Push image to registry
docker push myregistry.com/myapp:v1.0
```

### Container Operations
```bash
# Run container in detached mode
docker run -d \
  --name webapp \
  -p 8080:80 \
  -e NODE_ENV=production \
  -v /host/data:/app/data \
  myapp:v1.0

# Execute command in running container
docker exec -it webapp bash

# View container logs
docker logs webapp

# Follow log output
docker logs -f webapp

# Copy files to/from container
docker cp ./config.json webapp:/app/config.json
docker cp webapp:/app/logs ./logs

# View container processes
docker top webapp

# Monitor container stats
docker stats webapp
```

### Image Layers and Optimization
```bash
# View image layers
docker history --no-trunc myapp:v1.0

# Analyze image size
docker system df

# Remove unused images
docker image prune

# Remove all unused resources
docker system prune -a
```

## Dockerfile Best Practices {#dockerfile}

### Multi-stage Build Example
```dockerfile
# Build stage
FROM node:16-alpine AS builder

WORKDIR /app

# Copy package files first (better caching)
COPY package*.json ./
RUN npm ci --only=production

# Copy source code
COPY src/ ./src/
RUN npm run build

# Production stage
FROM nginx:1.21-alpine AS production

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Copy built application
COPY --from=builder --chown=nextjs:nodejs /app/dist /usr/share/nginx/html

# Copy custom nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Switch to non-root user
USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

# Start application
CMD ["nginx", "-g", "daemon off;"]
```

### Python Application Dockerfile
```dockerfile
FROM python:3.9-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN useradd --create-home --shell /bin/bash app

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=app:app . .

# Switch to app user
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Start application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "app:app"]
```

### Dockerfile Optimization Tips
```dockerfile
# 1. Use specific base image tags
FROM node:16.14.2-alpine3.15

# 2. Minimize layers by combining RUN commands
RUN apt-get update && \
    apt-get install -y curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 3. Order layers by frequency of change
COPY package*.json ./          # Changes less frequently
RUN npm install
COPY . .                       # Changes more frequently

# 4. Use .dockerignore
# Create .dockerignore file:
node_modules
.git
.gitignore
README.md
Dockerfile
.dockerignore

# 5. Use multi-stage builds for smaller images
FROM golang:1.19-alpine AS builder
# ... build steps ...

FROM alpine:3.16
COPY --from=builder /app/binary /usr/local/bin/
```

## Docker Networking {#networking}

### Network Types
```bash
# List networks
docker network ls

# Create custom bridge network
docker network create \
  --driver bridge \
  --subnet=172.20.0.0/16 \
  --ip-range=172.20.240.0/20 \
  mynetwork

# Create overlay network (for swarm)
docker network create \
  --driver overlay \
  --attachable \
  my-overlay

# Inspect network
docker network inspect mynetwork

# Connect container to network
docker network connect mynetwork webapp

# Disconnect container from network
docker network disconnect mynetwork webapp
```

### Container Communication
```bash
# Run containers on same network
docker run -d --name database --network mynetwork postgres:13
docker run -d --name backend --network mynetwork \
  -e DATABASE_URL=postgresql://user:pass@database:5432/db \
  myapi:v1.0

# Containers can communicate using container names as hostnames
# backend can reach database at hostname "database"
```

### Port Mapping
```bash
# Map container port to host port
docker run -p 8080:80 nginx        # Host:Container

# Map to specific interface
docker run -p 127.0.0.1:8080:80 nginx

# Map random port
docker run -P nginx

# Multiple port mappings
docker run -p 80:80 -p 443:443 nginx
```

### Network Security
```bash
# Create isolated network
docker network create --internal secure-network

# Run container with no network
docker run --network none alpine

# Limit container resources
docker run --memory=512m --cpus=1.5 myapp
```

## Volume Management {#volumes}

### Volume Types
```bash
# Named volumes (managed by Docker)
docker volume create mydata
docker run -v mydata:/app/data myapp

# Bind mounts (host directory)
docker run -v /host/path:/container/path myapp

# tmpfs mounts (temporary, in-memory)
docker run --tmpfs /tmp myapp
```

### Volume Operations
```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect mydata

# Remove volume
docker volume rm mydata

# Remove unused volumes
docker volume prune

# Backup volume data
docker run --rm \
  -v mydata:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/backup.tar.gz -C /data .

# Restore volume data
docker run --rm \
  -v mydata:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/backup.tar.gz -C /data
```

### Database Volume Example
```bash
# PostgreSQL with persistent data
docker run -d \
  --name postgres \
  -e POSTGRES_PASSWORD=secretpassword \
  -e POSTGRES_DB=myapp \
  -v postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13

# MySQL with persistent data
docker run -d \
  --name mysql \
  -e MYSQL_ROOT_PASSWORD=rootpassword \
  -e MYSQL_DATABASE=myapp \
  -v mysql_data:/var/lib/mysql \
  -p 3306:3306 \
  mysql:8.0
```

## Docker Compose {#compose}

### Basic docker-compose.yml
```yaml
version: '3.8'

services:
  # Web application
  web:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://user:password@db:5432/myapp
    depends_on:
      - db
      - redis
    networks:
      - app-network
    volumes:
      - ./uploads:/app/uploads
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Database
  db:
    image: postgres:13-alpine
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD_FILE=/run/secrets/db_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - app-network
    secrets:
      - db_password
    restart: unless-stopped

  # Redis cache
  redis:
    image: redis:6-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}
    networks:
      - app-network
    volumes:
      - redis_data:/data
    restart: unless-stopped

  # Nginx reverse proxy
  nginx:
    image: nginx:1.21-alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - web
    networks:
      - app-network
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:

networks:
  app-network:
    driver: bridge

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

### Development docker-compose.override.yml
```yaml
version: '3.8'

services:
  web:
    build:
      target: development
    environment:
      - NODE_ENV=development
      - DEBUG=app:*
    volumes:
      - .:/app
      - /app/node_modules
    ports:
      - "3000:3000"
      - "9229:9229"  # Debug port
    command: npm run dev

  db:
    ports:
      - "5432:5432"  # Expose for development tools

  redis:
    ports:
      - "6379:6379"
```

### Compose Commands
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f web

# Scale services
docker-compose up -d --scale web=3

# Execute command in service
docker-compose exec web bash

# Stop services
docker-compose stop

# Remove services and networks
docker-compose down

# Remove with volumes
docker-compose down -v

# Build images
docker-compose build

# Pull latest images
docker-compose pull
```

## Security Considerations {#security}

### Image Security
```dockerfile
# Use official base images
FROM node:16-alpine

# Keep base images updated
FROM ubuntu:20.04
RUN apt-get update && apt-get upgrade -y

# Don't run as root
RUN useradd -m -u 1001 appuser
USER appuser

# Use specific versions
FROM nginx:1.21.6-alpine

# Remove unnecessary packages
RUN apt-get remove -y build-essential && \
    apt-get autoremove -y && \
    apt-get clean
```

### Runtime Security
```bash
# Run with limited privileges
docker run --user 1001:1001 myapp

# Limit resources
docker run \
  --memory=512m \
  --cpus=1.0 \
  --pids-limit=100 \
  myapp

# Read-only root filesystem
docker run --read-only myapp

# No new privileges
docker run --security-opt=no-new-privileges myapp

# Drop capabilities
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE nginx

# Use security profiles
docker run --security-opt apparmor:docker-default myapp
```

### Secrets Management
```bash
# Docker secrets (Swarm mode)
echo "mysecretpassword" | docker secret create db_password -

# Environment files
docker run --env-file .env myapp

# External secret management
docker run \
  -e VAULT_ADDR=https://vault.company.com \
  -e VAULT_TOKEN_FILE=/run/secrets/vault_token \
  myapp
```

### Network Security
```bash
# Custom bridge network
docker network create --driver bridge isolated-network

# Internal network (no external access)
docker network create --internal internal-network

# Encrypted overlay network
docker network create \
  --driver overlay \
  --opt encrypted \
  secure-overlay
```

## Performance Optimization {#performance}

### Image Optimization
```dockerfile
# Multi-stage build to reduce size
FROM node:16-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:16-alpine AS runtime
COPY --from=builder /app/node_modules ./node_modules
COPY . .
EXPOSE 3000
CMD ["node", "index.js"]
```

### Container Resource Limits
```bash
# Memory limits
docker run -m 512m myapp

# CPU limits
docker run --cpus=1.5 myapp

# Combined limits
docker run \
  --memory=1g \
  --memory-swap=2g \
  --cpus=2.0 \
  --oom-kill-disable=false \
  myapp
```

### Monitoring and Logging
```bash
# Container stats
docker stats

# System information
docker system df
docker system events

# Log management
docker run \
  --log-driver=json-file \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  myapp

# Send logs to external system
docker run \
  --log-driver=syslog \
  --log-opt syslog-address=tcp://logserver:514 \
  myapp
```

### Performance Monitoring
```yaml
# docker-compose.yml with monitoring
version: '3.8'
services:
  app:
    image: myapp:latest
    
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

## Production Deployment {#production}

### Docker Swarm Setup
```bash
# Initialize swarm
docker swarm init

# Add worker nodes
docker swarm join --token <token> <manager-ip>:2377

# Deploy stack
docker stack deploy -c docker-compose.yml myapp

# List services
docker service ls

# Scale service
docker service scale myapp_web=5

# Update service
docker service update --image myapp:v2.0 myapp_web

# Remove stack
docker stack rm myapp
```

### Production docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    image: myregistry.com/myapp:${VERSION}
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
        failure_action: rollback
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 256M
          cpus: '0.25'
    networks:
      - web-network
    secrets:
      - app_secret
    configs:
      - source: app_config
        target: /app/config.json

  nginx:
    image: nginx:1.21-alpine
    deploy:
      replicas: 2
      placement:
        constraints:
          - node.role == manager
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /etc/ssl/certs:/etc/ssl/certs:ro
    configs:
      - source: nginx_config
        target: /etc/nginx/nginx.conf

networks:
  web-network:
    driver: overlay
    attachable: true

secrets:
  app_secret:
    external: true

configs:
  app_config:
    external: true
  nginx_config:
    external: true
```

### CI/CD Pipeline Example
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    tags:
      - 'v*'

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Build Docker image
      run: |
        docker build -t myregistry.com/myapp:${{ github.ref_name }} .
        
    - name: Run tests
      run: |
        docker run --rm myregistry.com/myapp:${{ github.ref_name }} npm test
        
    - name: Push to registry
      run: |
        echo ${{ secrets.REGISTRY_PASSWORD }} | docker login myregistry.com -u ${{ secrets.REGISTRY_USERNAME }} --password-stdin
        docker push myregistry.com/myapp:${{ github.ref_name }}
        
    - name: Deploy to production
      run: |
        ssh production-server "
          export VERSION=${{ github.ref_name }}
          docker stack deploy -c docker-compose.yml myapp
        "
```

### Health Checks and Monitoring
```bash
# Container health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

# Service health monitoring
docker service ps myapp_web
docker service logs myapp_web

# System monitoring
docker system df
docker system prune -a
```

### Backup and Recovery
```bash
# Backup volumes
docker run --rm \
  -v myapp_data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/data-$(date +%Y%m%d).tar.gz -C /data .

# Database backup
docker exec postgres pg_dump -U user myapp > backup.sql

# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker run --rm \
  -v postgres_data:/data \
  -v /backups:/backup \
  alpine tar czf /backup/postgres_$DATE.tar.gz -C /data .

# Keep only last 7 days of backups
find /backups -name "postgres_*.tar.gz" -mtime +7 -delete
```

This comprehensive Docker guide covers everything from basic concepts to production deployment. Docker containers provide a powerful way to package, distribute, and run applications consistently across different environments. By following these best practices, you'll be able to build secure, efficient, and scalable containerized applications.

Remember to keep your images updated, follow security best practices, monitor your containers in production, and always test your deployment processes before rolling them out to production environments.''',
            'category': 'DevOps',
            'tags': 'docker,containerization,devops,deployment',
        },
        {
            'title': 'Machine Learning with Scikit-Learn',
            'content': '''# Machine Learning with Scikit-Learn: Complete Guide

## Table of Contents
1. [Introduction to Scikit-Learn](#introduction)
2. [Data Preprocessing](#preprocessing)
3. [Supervised Learning](#supervised)
4. [Unsupervised Learning](#unsupervised)
5. [Model Evaluation](#evaluation)
6. [Feature Engineering](#features)
7. [Pipeline Creation](#pipelines)
8. [Model Selection](#selection)
9. [Advanced Techniques](#advanced)
10. [Production Deployment](#production)

## Introduction to Scikit-Learn {#introduction}

Scikit-learn is the most popular machine learning library for Python, providing simple and efficient tools for data mining and data analysis. It's built on NumPy, SciPy, and matplotlib and offers a consistent API for various machine learning algorithms.

### Key Features
- **Simple and efficient**: Easy-to-use API
- **Comprehensive**: Wide range of algorithms
- **Well-documented**: Excellent documentation and examples
- **Active community**: Regular updates and support
- **Production-ready**: Used in many production systems

### Installation and Setup
```python
# Install scikit-learn
pip install scikit-learn

# Import common modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
```

### Basic Workflow
```python
# 1. Load and explore data
from sklearn.datasets import load_iris
iris = load_iris()
X, y = iris.data, iris.target

# 2. Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. Choose and train model
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# 4. Make predictions
y_pred = model.predict(X_test)

# 5. Evaluate model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.3f}")
```

## Data Preprocessing {#preprocessing}

### Handling Missing Data
```python
import pandas as pd
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

# Sample data with missing values
data = pd.DataFrame({
    'age': [25, 30, np.nan, 35, 40],
    'income': [50000, np.nan, 75000, 80000, np.nan],
    'score': [85, 90, 88, np.nan, 92]
})

# Simple imputation strategies
# Mean imputation
mean_imputer = SimpleImputer(strategy='mean')
data_mean_imputed = pd.DataFrame(
    mean_imputer.fit_transform(data),
    columns=data.columns
)

# Median imputation
median_imputer = SimpleImputer(strategy='median')
data_median_imputed = pd.DataFrame(
    median_imputer.fit_transform(data),
    columns=data.columns
)

# Mode imputation (for categorical data)
mode_imputer = SimpleImputer(strategy='most_frequent')

# KNN imputation
knn_imputer = KNNImputer(n_neighbors=2)
data_knn_imputed = pd.DataFrame(
    knn_imputer.fit_transform(data),
    columns=data.columns
)

# Iterative imputation (MICE)
iterative_imputer = IterativeImputer(random_state=42)
data_iterative_imputed = pd.DataFrame(
    iterative_imputer.fit_transform(data),
    columns=data.columns
)
```

### Feature Scaling
```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.preprocessing import PowerTransformer, QuantileTransformer

# Sample data
X = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9],
              [10, 11, 12]])

# Standard Scaling (z-score normalization)
standard_scaler = StandardScaler()
X_standard = standard_scaler.fit_transform(X)
print("Standard scaled:")
print(X_standard)

# Min-Max Scaling (0-1 normalization)
minmax_scaler = MinMaxScaler()
X_minmax = minmax_scaler.fit_transform(X)
print("Min-Max scaled:")
print(X_minmax)

# Robust Scaling (uses median and IQR)
robust_scaler = RobustScaler()
X_robust = robust_scaler.fit_transform(X)
print("Robust scaled:")
print(X_robust)

# Power Transformer (Yeo-Johnson)
power_transformer = PowerTransformer(method='yeo-johnson')
X_power = power_transformer.fit_transform(X)

# Quantile Transformer (uniform distribution)
quantile_transformer = QuantileTransformer(output_distribution='uniform')
X_quantile = quantile_transformer.fit_transform(X)
```

### Encoding Categorical Variables
```python
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer
import pandas as pd

# Sample categorical data
data = pd.DataFrame({
    'color': ['red', 'blue', 'green', 'red', 'blue'],
    'size': ['S', 'M', 'L', 'M', 'S'],
    'rating': ['good', 'excellent', 'poor', 'good', 'excellent']
})

# Label Encoding (for ordinal categories)
label_encoder = LabelEncoder()
data['size_encoded'] = label_encoder.fit_transform(data['size'])

# Ordinal Encoding (with custom order)
ordinal_encoder = OrdinalEncoder(
    categories=[['poor', 'good', 'excellent']]
)
data['rating_encoded'] = ordinal_encoder.fit_transform(
    data[['rating']]
).flatten()

# One-Hot Encoding
onehot_encoder = OneHotEncoder(sparse=False, drop='first')
color_encoded = onehot_encoder.fit_transform(data[['color']])
color_feature_names = onehot_encoder.get_feature_names_out(['color'])

# Add one-hot encoded features to dataframe
for i, feature_name in enumerate(color_feature_names):
    data[feature_name] = color_encoded[:, i]

print(data)
```

### Feature Selection
```python
from sklearn.feature_selection import (
    SelectKBest, f_classif, mutual_info_classif,
    RFE, SelectFromModel
)
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import Lasso

# Load example data
from sklearn.datasets import load_breast_cancer
data = load_breast_cancer()
X, y = data.data, data.target

# Univariate feature selection
selector_kbest = SelectKBest(score_func=f_classif, k=10)
X_kbest = selector_kbest.fit_transform(X, y)

# Get selected feature indices
selected_features = selector_kbest.get_support(indices=True)
print(f"Selected features: {selected_features}")

# Recursive Feature Elimination (RFE)
estimator = RandomForestClassifier(random_state=42)
rfe_selector = RFE(estimator=estimator, n_features_to_select=10)
X_rfe = rfe_selector.fit_transform(X, y)

# Feature selection based on model importance
lasso = Lasso(alpha=0.01, random_state=42)
sfm_selector = SelectFromModel(lasso)
X_sfm = sfm_selector.fit_transform(X, y)

print(f"Original features: {X.shape[1]}")
print(f"K-best features: {X_kbest.shape[1]}")
print(f"RFE features: {X_rfe.shape[1]}")
print(f"SelectFromModel features: {X_sfm.shape[1]}")
```

## Supervised Learning {#supervised}

### Classification Algorithms
```python
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Load dataset
from sklearn.datasets import load_wine
wine = load_wine()
X, y = wine.data, wine.target

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Dictionary of classifiers
classifiers = {
    'Logistic Regression': LogisticRegression(random_state=42),
    'Decision Tree': DecisionTreeClassifier(random_state=42),
    'Random Forest': RandomForestClassifier(random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(random_state=42),
    'SVM': SVC(random_state=42),
    'Naive Bayes': GaussianNB(),
    'KNN': KNeighborsClassifier()
}

# Train and evaluate each classifier
results = {}
for name, clf in classifiers.items():
    # Use scaled data for algorithms that need it
    if name in ['Logistic Regression', 'SVM', 'KNN']:
        clf.fit(X_train_scaled, y_train)
        y_pred = clf.predict(X_test_scaled)
    else:
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    results[name] = accuracy
    
    print(f"{name} Accuracy: {accuracy:.3f}")
    print(f"Classification Report for {name}:")
    print(classification_report(y_test, y_pred))
    print("-" * 50)

# Find best classifier
best_classifier = max(results, key=results.get)
print(f"Best classifier: {best_classifier} with accuracy: {results[best_classifier]:.3f}")
```

### Regression Algorithms
```python
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# Load dataset
from sklearn.datasets import load_boston
boston = load_boston()
X, y = boston.data, boston.target

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Dictionary of regressors
regressors = {
    'Linear Regression': LinearRegression(),
    'Ridge Regression': Ridge(alpha=1.0),
    'Lasso Regression': Lasso(alpha=1.0),
    'Elastic Net': ElasticNet(alpha=1.0, l1_ratio=0.5),
    'Decision Tree': DecisionTreeRegressor(random_state=42),
    'Random Forest': RandomForestRegressor(random_state=42),
    'Gradient Boosting': GradientBoostingRegressor(random_state=42),
    'SVR': SVR(),
    'KNN': KNeighborsRegressor()
}

# Train and evaluate each regressor
results = {}
for name, reg in regressors.items():
    # Use scaled data for algorithms that need it
    if name in ['Linear Regression', 'Ridge Regression', 'Lasso Regression', 
                'Elastic Net', 'SVR', 'KNN']:
        reg.fit(X_train_scaled, y_train)
        y_pred = reg.predict(X_test_scaled)
    else:
        reg.fit(X_train, y_train)
        y_pred = reg.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    results[name] = {
        'MSE': mse,
        'RMSE': rmse,
        'MAE': mae,
        'R²': r2
    }
    
    print(f"{name}:")
    print(f"  MSE: {mse:.3f}")
    print(f"  RMSE: {rmse:.3f}")
    print(f"  MAE: {mae:.3f}")
    print(f"  R²: {r2:.3f}")
    print("-" * 30)
```

## Unsupervised Learning {#unsupervised}

### Clustering Algorithms
```python
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, adjusted_rand_score
import matplotlib.pyplot as plt

# Generate sample data
from sklearn.datasets import make_blobs
X, y_true = make_blobs(n_samples=300, centers=4, n_features=2,
                       random_state=42, cluster_std=0.60)

# K-Means Clustering
kmeans = KMeans(n_clusters=4, random_state=42)
y_kmeans = kmeans.fit_predict(X)

# DBSCAN Clustering
dbscan = DBSCAN(eps=0.3, min_samples=10)
y_dbscan = dbscan.fit_predict(X)

# Hierarchical Clustering
hierarchical = AgglomerativeClustering(n_clusters=4)
y_hierarchical = hierarchical.fit_predict(X)

# Gaussian Mixture Model
gmm = GaussianMixture(n_components=4, random_state=42)
y_gmm = gmm.fit_predict(X)

# Evaluate clustering results
clustering_results = {
    'K-Means': y_kmeans,
    'DBSCAN': y_dbscan,
    'Hierarchical': y_hierarchical,
    'GMM': y_gmm
}

for name, labels in clustering_results.items():
    if len(set(labels)) > 1:  # Check if clustering found more than one cluster
        silhouette = silhouette_score(X, labels)
        ari = adjusted_rand_score(y_true, labels)
        print(f"{name}:")
        print(f"  Silhouette Score: {silhouette:.3f}")
        print(f"  Adjusted Rand Index: {ari:.3f}")
        print(f"  Number of clusters: {len(set(labels))}")
    else:
        print(f"{name}: Failed to find multiple clusters")
    print("-" * 30)

# Plotting results
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle('Clustering Results')

for i, (name, labels) in enumerate(clustering_results.items()):
    row = i // 2
    col = i % 2
    scatter = axes[row, col].scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis')
    axes[row, col].set_title(name)
    axes[row, col].set_xlabel('Feature 1')
    axes[row, col].set_ylabel('Feature 2')

plt.tight_layout()
plt.show()
```

### Dimensionality Reduction
```python
from sklearn.decomposition import PCA, TruncatedSVD, FastICA
from sklearn.manifold import TSNE, Isomap
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import matplotlib.pyplot as plt

# Load high-dimensional dataset
from sklearn.datasets import load_digits
digits = load_digits()
X, y = digits.data, digits.target

print(f"Original shape: {X.shape}")

# Principal Component Analysis (PCA)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)
print(f"PCA explained variance ratio: {pca.explained_variance_ratio_}")

# Linear Discriminant Analysis (LDA)
lda = LinearDiscriminantAnalysis(n_components=2)
X_lda = lda.fit_transform(X, y)

# t-SNE
tsne = TSNE(n_components=2, random_state=42, perplexity=30)
X_tsne = tsne.fit_transform(X)

# Isomap
isomap = Isomap(n_components=2)
X_isomap = isomap.fit_transform(X)

# Independent Component Analysis (ICA)
ica = FastICA(n_components=2, random_state=42)
X_ica = ica.fit_transform(X)

# Plot results
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle('Dimensionality Reduction Techniques')

techniques = [
    ('PCA', X_pca),
    ('LDA', X_lda),
    ('t-SNE', X_tsne),
    ('Isomap', X_isomap),
    ('ICA', X_ica)
]

for i, (name, X_reduced) in enumerate(techniques):
    if i < 6:  # We only have 6 subplots
        row = i // 3
        col = i % 3
        scatter = axes[row, col].scatter(X_reduced[:, 0], X_reduced[:, 1], 
                                       c=y, cmap='tab10', alpha=0.7)
        axes[row, col].set_title(name)
        axes[row, col].set_xlabel('Component 1')
        axes[row, col].set_ylabel('Component 2')

# Remove empty subplot
fig.delaxes(axes[1, 2])

plt.tight_layout()
plt.show()

# PCA with explained variance analysis
pca_full = PCA()
pca_full.fit(X)

# Plot cumulative explained variance
plt.figure(figsize=(10, 6))
cumsum = np.cumsum(pca_full.explained_variance_ratio_)
plt.plot(range(1, len(cumsum) + 1), cumsum, 'bo-')
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance Ratio')
plt.title('PCA Explained Variance')
plt.grid(True)

# Find number of components for 95% variance
n_components_95 = np.argmax(cumsum >= 0.95) + 1
plt.axhline(y=0.95, color='r', linestyle='--', label='95% Variance')
plt.axvline(x=n_components_95, color='r', linestyle='--', 
           label=f'{n_components_95} Components')
plt.legend()
plt.show()

print(f"Number of components for 95% variance: {n_components_95}")
```

## Model Evaluation {#evaluation}

### Cross-Validation
```python
from sklearn.model_selection import (
    cross_val_score, cross_validate, StratifiedKFold,
    TimeSeriesSplit, LeaveOneOut, ShuffleSplit
)
from sklearn.metrics import make_scorer, f1_score

# Load dataset
from sklearn.datasets import load_breast_cancer
data = load_breast_cancer()
X, y = data.data, data.target

# Simple cross-validation
model = RandomForestClassifier(random_state=42)
cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')

print(f"Cross-validation scores: {cv_scores}")
print(f"Mean CV score: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")

# Stratified K-Fold (maintains class distribution)
stratified_kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
stratified_scores = cross_val_score(model, X, y, cv=stratified_kfold, scoring='accuracy')

print(f"Stratified CV scores: {stratified_scores}")
print(f"Mean Stratified CV score: {stratified_scores.mean():.3f}")

# Multiple scoring metrics
scoring = ['accuracy', 'precision_macro', 'recall_macro', 'f1_macro']
cv_results = cross_validate(model, X, y, cv=5, scoring=scoring)

for metric in scoring:
    scores = cv_results[f'test_{metric}']
    print(f"{metric}: {scores.mean():.3f} (+/- {scores.std() * 2:.3f})")

# Custom scoring function
def custom_f1_score(y_true, y_pred):
    return f1_score(y_true, y_pred, average='weighted')

custom_scorer = make_scorer(custom_f1_score)
custom_scores = cross_val_score(model, X, y, cv=5, scoring=custom_scorer)
print(f"Custom F1 scores: {custom_scores.mean():.3f}")
```

### Performance Metrics
```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, precision_recall_curve,
    confusion_matrix, classification_report
)
import matplotlib.pyplot as plt

# Train a model
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

# Basic metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_pred_proba)

print(f"Accuracy: {accuracy:.3f}")
print(f"Precision: {precision:.3f}")
print(f"Recall: {recall:.3f}")
print(f"F1-score: {f1:.3f}")
print(f"AUC-ROC: {auc:.3f}")

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

# ROC Curve
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {auc:.3f})')
plt.plot([0, 1], [0, 1], 'k--', label='Random')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()
plt.grid(True)
plt.show()

# Precision-Recall Curve
precision_vals, recall_vals, pr_thresholds = precision_recall_curve(y_test, y_pred_proba)
plt.figure(figsize=(8, 6))
plt.plot(recall_vals, precision_vals, label='Precision-Recall Curve')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.legend()
plt.grid(True)
plt.show()

# Detailed classification report
print("Classification Report:")
print(classification_report(y_test, y_pred))
```

This comprehensive guide covers the fundamental aspects of machine learning with scikit-learn. The library's consistent API and extensive documentation make it an excellent choice for both beginners and experienced practitioners. Remember to always validate your models properly, understand your data, and choose appropriate algorithms for your specific problem domain.''',
            'category': 'Data Science',
            'tags': 'machine-learning,scikit-learn,python,data-science',
        },
        {
            'title': 'Git Workflow Best Practices',
            'content': '''# Git Workflow Best Practices: Professional Version Control

## Table of Contents
1. [Git Fundamentals](#fundamentals)
2. [Branching Strategies](#branching)
3. [Commit Best Practices](#commits)
4. [Collaboration Workflows](#collaboration)
5. [Code Review Process](#reviews)
6. [Release Management](#releases)
7. [Conflict Resolution](#conflicts)
8. [Git Hooks and Automation](#hooks)
9. [Advanced Git Techniques](#advanced)
10. [Best Practices Summary](#summary)

## Git Fundamentals {#fundamentals}

Git is a distributed version control system that tracks changes in source code during software development. Understanding Git fundamentals is crucial for effective collaboration and code management.

### Basic Git Configuration
```bash
# Global configuration
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global init.defaultBranch main

# Editor configuration
git config --global core.editor "code --wait"

# Line ending configuration
git config --global core.autocrlf input  # macOS/Linux
git config --global core.autocrlf true   # Windows

# Useful aliases
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual '!gitk'
```

### Repository Initialization
```bash
# Initialize new repository
git init
git add .
git commit -m "Initial commit"

# Clone existing repository
git clone https://github.com/user/repository.git
cd repository

# Add remote to existing repository
git remote add origin https://github.com/user/repository.git
git branch -M main
git push -u origin main
```

## Branching Strategies {#branching}

### Git Flow
Git Flow is a branching model that defines specific branch types and their purposes:

```bash
# Main branches
# - main/master: Production-ready code
# - develop: Integration branch for features

# Supporting branches
# - feature/*: New features
# - release/*: Release preparation
# - hotfix/*: Critical fixes

# Initialize Git Flow
git flow init

# Feature branches
git flow feature start new-login-system
# Work on feature...
git flow feature finish new-login-system

# Release branches
git flow release start 1.2.0
# Prepare release...
git flow release finish 1.2.0

# Hotfix branches
git flow hotfix start critical-security-fix
# Fix the issue...
git flow hotfix finish critical-security-fix
```

### GitHub Flow (Simplified)
```bash
# Create feature branch from main
git checkout main
git pull origin main
git checkout -b feature/user-authentication

# Work on feature
git add .
git commit -m "Add user authentication endpoints"
git push origin feature/user-authentication

# Create pull request on GitHub
# After review and approval, merge to main
# Delete feature branch
git checkout main
git pull origin main
git branch -d feature/user-authentication
```

### GitLab Flow
```bash
# Feature branch workflow
git checkout -b feature/payment-integration

# Environment branches
git checkout -b production  # Production environment
git checkout -b staging     # Staging environment
git checkout -b develop     # Development environment

# Release branch with environment promotion
git checkout main
git checkout -b release/1.3.0
# Deploy to staging for testing
# After testing, merge to production
```

## Commit Best Practices {#commits}

### Conventional Commits
Follow the Conventional Commits specification for consistent commit messages:

```bash
# Format: <type>[optional scope]: <description>
# [optional body]
# [optional footer(s)]

# Types:
# feat: New feature
# fix: Bug fix
# docs: Documentation changes
# style: Code style changes (formatting, etc.)
# refactor: Code refactoring
# test: Adding or updating tests
# chore: Maintenance tasks

# Examples:
git commit -m "feat(auth): add OAuth2 authentication"
git commit -m "fix(api): handle null response in user endpoint"
git commit -m "docs: update API documentation for v2"
git commit -m "refactor(database): optimize user queries"
git commit -m "test(auth): add unit tests for login functionality"

# Multi-line commit with body
git commit -m "feat(payment): integrate Stripe payment processing

Add Stripe payment integration with the following features:
- Credit card processing
- Subscription management
- Webhook handling for payment events

Closes #123"
```

### Atomic Commits
Make commits that represent single, logical changes:

```bash
# Good: Single logical change
git add src/auth/login.js
git commit -m "feat(auth): add login validation"

# Bad: Multiple unrelated changes
git add .
git commit -m "fix login, update docs, refactor database"

# Use interactive staging for partial commits
git add -p  # Stage hunks interactively
git commit -m "feat(auth): add email validation"

# Amend last commit (if not pushed)
git add forgotten-file.js
git commit --amend --no-edit
```

### Commit Message Templates
Create a commit message template:

```bash
# Create template file
cat > ~/.gitmessage << EOF
# Title: Summary, imperative, start upper case, don't end with a period
# No more than 50 chars. #### 50 chars is here:  #

# Remember blank line between title and body.

# Body: Explain *what* and *why* (not *how*). Include task ID (Jira issue).
# Wrap at 72 chars. ################################## which is here:  #


# At the end: Include Co-authored-by for all contributors. 
# Include at least one empty line before it. Format: 
# Co-authored-by: name <user@users.noreply.github.com>
#
# How to Write a Git Commit Message:
# https://chris.beams.io/posts/git-commit/
#
# 1. Separate subject from body with a blank line
# 2. Limit the subject line to 50 characters
# 3. Capitalize the subject line
# 4. Do not end the subject line with a period
# 5. Use the imperative mood in the subject line
# 6. Wrap the body at 72 characters
# 7. Use the body to explain what and why vs. how
EOF

# Configure Git to use the template
git config --global commit.template ~/.gitmessage
```

## Collaboration Workflows {#collaboration}

### Fork and Pull Request Workflow
```bash
# Fork repository on GitHub/GitLab
# Clone your fork
git clone https://github.com/yourusername/repository.git
cd repository

# Add upstream remote
git remote add upstream https://github.com/originalowner/repository.git

# Create feature branch
git checkout -b feature/awesome-feature

# Keep your fork up to date
git fetch upstream
git checkout main
git merge upstream/main
git push origin main

# Work on your feature
git add .
git commit -m "feat: add awesome feature"
git push origin feature/awesome-feature

# Create pull request
# After merge, clean up
git checkout main
git pull upstream main
git branch -d feature/awesome-feature
git push origin --delete feature/awesome-feature
```

### Collaborative Feature Development
```bash
# Multiple developers on same feature
git checkout -b feature/complex-feature

# Developer A pushes initial work
git push origin feature/complex-feature

# Developer B joins the feature
git fetch origin
git checkout feature/complex-feature

# Regular synchronization
git pull origin feature/complex-feature
# Work on your part
git add .
git commit -m "feat(feature): add component X"
git push origin feature/complex-feature

# Resolve conflicts when they occur
git pull origin feature/complex-feature
# Resolve conflicts in editor
git add resolved-file.js
git commit -m "resolve: merge conflicts in feature branch"
git push origin feature/complex-feature
```

## Code Review Process {#reviews}

### Preparing Code for Review
```bash
# Clean up commit history before creating PR
git rebase -i HEAD~3  # Interactive rebase for last 3 commits

# Squash related commits
pick a1b2c3d feat: add user model
squash e4f5g6h feat: add user validation
squash h7i8j9k feat: add user tests

# Update commit message
# This will become: "feat: add user model with validation and tests"

# Force push clean history (only on feature branches)
git push --force-with-lease origin feature/user-management
```

### Review Checklist
```markdown
## Code Review Checklist

### Functionality
- [ ] Code works as intended
- [ ] Edge cases are handled
- [ ] Error handling is appropriate
- [ ] Performance considerations

### Code Quality
- [ ] Code is readable and well-structured
- [ ] Functions are appropriately sized
- [ ] Variable names are descriptive
- [ ] Comments explain why, not what

### Testing
- [ ] Unit tests are included
- [ ] Tests cover edge cases
- [ ] Integration tests if needed
- [ ] All tests pass

### Security
- [ ] No sensitive data in code
- [ ] Input validation present
- [ ] Authentication/authorization checked
- [ ] SQL injection prevention

### Documentation
- [ ] README updated if needed
- [ ] API documentation updated
- [ ] Inline comments for complex logic
- [ ] CHANGELOG updated
```

## Release Management {#releases}

### Semantic Versioning
```bash
# Version format: MAJOR.MINOR.PATCH
# MAJOR: Breaking changes
# MINOR: New features (backward compatible)
# PATCH: Bug fixes (backward compatible)

# Examples:
# 1.0.0 -> 1.0.1 (bug fix)
# 1.0.1 -> 1.1.0 (new feature)
# 1.1.0 -> 2.0.0 (breaking change)

# Tag releases
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin v1.2.0

# List tags
git tag -l

# Checkout specific version
git checkout v1.2.0
```

### Release Branch Workflow
```bash
# Create release branch
git checkout develop
git pull origin develop
git checkout -b release/1.3.0

# Prepare release
# - Update version numbers
# - Update CHANGELOG
# - Final testing

# Merge to main and tag
git checkout main
git merge --no-ff release/1.3.0
git tag -a v1.3.0 -m "Release 1.3.0"

# Merge back to develop
git checkout develop
git merge --no-ff release/1.3.0

# Push everything
git push origin main
git push origin develop
git push origin v1.3.0

# Clean up
git branch -d release/1.3.0
git push origin --delete release/1.3.0
```

### Automated Release with GitHub Actions
```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Create Release
      uses: actions/create-release@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        tag_name: ${{ github.ref }}
        release_name: Release ${{ github.ref }}
        draft: false
        prerelease: false
```

## Conflict Resolution {#conflicts}

### Merge Conflicts
```bash
# When conflicts occur during merge
git merge feature-branch
# Auto-merging file.txt
# CONFLICT (content): Merge conflict in file.txt

# View conflict status
git status

# Resolve conflicts manually
# Edit file.txt to resolve conflicts
# Remove conflict markers: <<<<<<<, =======, >>>>>>>

# Mark as resolved
git add file.txt
git commit -m "resolve: merge conflicts from feature-branch"

# Use merge tools
git config --global merge.tool vimdiff
git mergetool
```

### Rebase Conflicts
```bash
# Interactive rebase with conflicts
git rebase -i HEAD~3

# When conflict occurs during rebase
# Edit conflicted files
git add resolved-file.txt
git rebase --continue

# Abort rebase if needed
git rebase --abort

# Skip problematic commit
git rebase --skip
```

### Advanced Conflict Resolution
```bash
# Use different merge strategies
git merge -X ours feature-branch    # Prefer current branch
git merge -X theirs feature-branch  # Prefer incoming changes

# Cherry-pick with conflict resolution
git cherry-pick abc123
# Resolve conflicts
git add .
git cherry-pick --continue

# Three-way merge understanding
git show :1:file.txt  # Common ancestor
git show :2:file.txt  # Current branch (ours)
git show :3:file.txt  # Incoming branch (theirs)
```

## Git Hooks and Automation {#hooks}

### Pre-commit Hooks
```bash
# Install pre-commit framework
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.1.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-merge-conflict
      - id: no-commit-to-branch
        args: ['--branch', 'main']
  
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
        language_version: python3.9
  
  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
EOF

# Install hooks
pre-commit install

# Run on all files
pre-commit run --all-files
```

### Custom Hooks
```bash
# Pre-commit hook script
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Run tests before commit
echo "Running tests..."
npm test
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi

# Run linting
echo "Running linter..."
npm run lint
if [ $? -ne 0 ]; then
    echo "Linting failed. Commit aborted."
    exit 1
fi

echo "All checks passed. Proceeding with commit."
EOF

chmod +x .git/hooks/pre-commit
```

### Commit Message Hooks
```bash
# Commit message validation
cat > .git/hooks/commit-msg << 'EOF'
#!/bin/bash
# Check commit message format
commit_regex='^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .{1,50}'

if ! grep -qE "$commit_regex" "$1"; then
    echo "Invalid commit message format!"
    echo "Format: type(scope): description"
    echo "Example: feat(auth): add login functionality"
    exit 1
fi
EOF

chmod +x .git/hooks/commit-msg
```

## Advanced Git Techniques {#advanced}

### Interactive Rebase
```bash
# Rewrite commit history
git rebase -i HEAD~5

# Options in interactive mode:
# pick = use commit
# reword = use commit, but edit message
# edit = use commit, but stop for amending
# squash = use commit, but meld into previous
# fixup = like squash, but discard log message
# drop = remove commit

# Example rebase plan:
pick a1b2c3d Add user authentication
squash e4f5g6h Fix authentication bug
reword h7i8j9k Add user registration
drop k9l0m1n Remove debug code
edit n2o3p4q Add password validation
```

### Advanced Log and History
```bash
# Pretty log formatting
git log --oneline --graph --decorate --all
git log --pretty=format:"%h %ad | %s%d [%an]" --graph --date=short

# Search commits
git log --grep="fix"              # Search commit messages
git log -S"function_name"         # Search code changes
git log --author="John Doe"       # Filter by author
git log --since="2 weeks ago"     # Time-based filtering
git log file.txt                  # Changes to specific file

# Show file evolution
git log -p file.txt               # Show patches
git blame file.txt                # Line-by-line author info
git show HEAD:file.txt            # Show file at specific commit
```

### Reflog and Recovery
```bash
# View reference log
git reflog

# Recover lost commits
git checkout abc123               # Detached HEAD
# Make some commits
git checkout main                 # Commits seem lost
git reflog                        # Find the lost commits
git checkout -b recover-branch abc123  # Recover them

# Undo various operations
git reset --hard HEAD~1           # Undo last commit
git reflog                        # Find the commit hash
git reset --hard abc123           # Restore to that commit
```

### Stashing Workflows
```bash
# Basic stashing
git stash push -m "Work in progress on feature X"
git stash list
git stash apply stash@{0}
git stash drop stash@{0}
git stash pop  # Apply and drop

# Partial stashing
git stash push -p  # Interactive stashing
git stash push --keep-index  # Stash only unstaged changes

# Stash untracked files
git stash push -u -m "Include untracked files"

# Create branch from stash
git stash branch feature-branch stash@{0}
```

## Best Practices Summary {#summary}

### Repository Structure
```
project/
├── .gitignore          # Ignore patterns
├── .gitattributes      # Git attributes
├── README.md           # Project documentation
├── CONTRIBUTING.md     # Contribution guidelines
├── CHANGELOG.md        # Change history
├── LICENSE            # Project license
└── .github/           # GitHub-specific files
    ├── workflows/     # GitHub Actions
    ├── ISSUE_TEMPLATE/
    └── PULL_REQUEST_TEMPLATE.md
```

### Essential .gitignore Patterns
```gitignore
# Dependencies
node_modules/
__pycache__/
.env

# Build outputs
dist/
build/
*.log

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Temporary files
*.tmp
*.temp
.cache/
```

### Workflow Guidelines
1. **Keep commits atomic** - One logical change per commit
2. **Write meaningful commit messages** - Follow conventional commits
3. **Use feature branches** - Never commit directly to main
4. **Review code thoroughly** - Use pull/merge requests
5. **Test before merging** - Automated testing in CI/CD
6. **Keep history clean** - Use rebase for feature branches
7. **Tag releases** - Use semantic versioning
8. **Document changes** - Maintain CHANGELOG
9. **Secure sensitive data** - Never commit secrets
10. **Backup important work** - Push regularly to remote

This comprehensive guide covers professional Git workflows that scale from individual projects to large team collaborations. Following these practices will lead to better code quality, easier collaboration, and more maintainable project history.''',
            'category': 'Tools',
            'tags': 'git,version-control,collaboration,workflow',
        },
        {
            'title': 'Web Security Fundamentals',
            'content': '''# Web Security Fundamentals: Comprehensive Protection Guide

## Table of Contents
1. [Introduction to Web Security](#introduction)
2. [Common Web Vulnerabilities](#vulnerabilities)
3. [Authentication and Authorization](#auth)
4. [Secure Communication (HTTPS/TLS)](#https)
5. [Input Validation and Sanitization](#validation)
6. [Session Management](#sessions)
7. [Cross-Site Scripting (XSS) Prevention](#xss)
8. [SQL Injection Prevention](#sql-injection)
9. [Cross-Site Request Forgery (CSRF) Protection](#csrf)
10. [Security Headers and Content Security Policy](#headers)
11. [Secure Development Practices](#practices)
12. [Security Testing and Monitoring](#testing)

## Introduction to Web Security {#introduction}

Web security is the practice of protecting websites, web applications, and web services from cyber threats. With the increasing sophistication of attacks and the growing reliance on web applications, security must be built into every layer of web development.

### The Security Mindset
- **Defense in Depth**: Multiple layers of security controls
- **Principle of Least Privilege**: Minimal access rights
- **Fail Securely**: Secure defaults when systems fail
- **Don't Trust User Input**: Validate everything
- **Security by Design**: Build security from the ground up

### OWASP Top 10 2021
The Open Web Application Security Project (OWASP) Top 10 represents the most critical web application security risks:

1. **A01:2021 – Broken Access Control**
2. **A02:2021 – Cryptographic Failures**
3. **A03:2021 – Injection**
4. **A04:2021 – Insecure Design**
5. **A05:2021 – Security Misconfiguration**
6. **A06:2021 – Vulnerable and Outdated Components**
7. **A07:2021 – Identification and Authentication Failures**
8. **A08:2021 – Software and Data Integrity Failures**
9. **A09:2021 – Security Logging and Monitoring Failures**
10. **A10:2021 – Server-Side Request Forgery (SSRF)**

## Common Web Vulnerabilities {#vulnerabilities}

### Injection Attacks
```python
# SQL Injection Example (VULNERABLE)
def get_user_data(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return execute_query(query)

# Attacker input: "1 OR 1=1" exposes all users

# SECURE: Parameterized queries
def get_user_data_secure(user_id):
    query = "SELECT * FROM users WHERE id = %s"
    return execute_query(query, (user_id,))

# NoSQL Injection Prevention
def find_user_secure(username):
    # VULNERABLE
    # db.users.find({"username": request.form["username"]})
    
    # SECURE
    if not isinstance(username, str):
        raise ValueError("Username must be a string")
    
    return db.users.find({"username": username})
```

### Cross-Site Scripting (XSS)
```javascript
// Reflected XSS Example (VULNERABLE)
app.get('/search', (req, res) => {
    const query = req.query.q;
    res.send(`<h1>Search results for: ${query}</h1>`);
});

// Attacker URL: /search?q=<script>alert('XSS')</script>

// SECURE: HTML escaping
const escapeHtml = (unsafe) => {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
};

app.get('/search', (req, res) => {
    const query = escapeHtml(req.query.q || '');
    res.send(`<h1>Search results for: ${query}</h1>`);
});

// Stored XSS Prevention
function sanitizeComment(comment) {
    // Use a library like DOMPurify
    return DOMPurify.sanitize(comment, {
        ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'p'],
        ALLOWED_ATTR: []
    });
}
```

### Cross-Site Request Forgery (CSRF)
```javascript
// CSRF Protection with tokens
const csrf = require('csrf');
const tokens = new csrf();

// Generate CSRF token
app.use((req, res, next) => {
    if (!req.session.csrfSecret) {
        req.session.csrfSecret = tokens.secretSync();
    }
    res.locals.csrfToken = tokens.create(req.session.csrfSecret);
    next();
});

// Validate CSRF token
function validateCSRF(req, res, next) {
    const token = req.body.csrfToken || req.headers['x-csrf-token'];
    if (!tokens.verify(req.session.csrfSecret, token)) {
        return res.status(403).json({ error: 'Invalid CSRF token' });
    }
    next();
}

// Protected route
app.post('/transfer-money', validateCSRF, (req, res) => {
    // Process money transfer
});

// HTML form with CSRF token
`<form method="POST" action="/transfer-money">
    <input type="hidden" name="csrfToken" value="${csrfToken}">
    <input type="number" name="amount" required>
    <button type="submit">Transfer</button>
</form>`
```

## Authentication and Authorization {#auth}

### Secure Password Handling
```python
import bcrypt
import secrets
from datetime import datetime, timedelta

class PasswordManager:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt."""
        # Generate salt and hash password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify password against hash."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    @staticmethod
    def generate_secure_token() -> str:
        """Generate cryptographically secure random token."""
        return secrets.token_urlsafe(32)

# Password strength validation
def validate_password_strength(password: str) -> dict:
    """Validate password meets security requirements."""
    errors = []
    
    if len(password) < 12:
        errors.append("Password must be at least 12 characters long")
    
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain uppercase letters")
    
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain lowercase letters")
    
    if not re.search(r'\d', password):
        errors.append("Password must contain numbers")
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Password must contain special characters")
    
    # Check against common passwords
    if check_common_password(password):
        errors.append("Password is too common")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }

# Account lockout protection
class AccountLockout:
    def __init__(self, max_attempts=5, lockout_duration=900):  # 15 minutes
        self.max_attempts = max_attempts
        self.lockout_duration = lockout_duration
        self.failed_attempts = {}
    
    def record_failed_attempt(self, username: str):
        """Record a failed login attempt."""
        now = datetime.now()
        if username not in self.failed_attempts:
            self.failed_attempts[username] = []
        
        self.failed_attempts[username].append(now)
        
        # Clean old attempts
        cutoff = now - timedelta(seconds=self.lockout_duration)
        self.failed_attempts[username] = [
            attempt for attempt in self.failed_attempts[username]
            if attempt > cutoff
        ]
    
    def is_locked(self, username: str) -> bool:
        """Check if account is locked."""
        if username not in self.failed_attempts:
            return False
        
        recent_attempts = len(self.failed_attempts[username])
        return recent_attempts >= self.max_attempts
    
    def clear_attempts(self, username: str):
        """Clear failed attempts after successful login."""
        if username in self.failed_attempts:
            del self.failed_attempts[username]
```

### Multi-Factor Authentication (MFA)
```python
import pyotp
import qrcode
from io import BytesIO

class MFAManager:
    @staticmethod
    def generate_secret() -> str:
        """Generate TOTP secret for user."""
        return pyotp.random_base32()
    
    @staticmethod
    def generate_qr_code(user_email: str, secret: str, issuer: str = "MyApp") -> bytes:
        """Generate QR code for TOTP setup."""
        totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=user_email,
            issuer_name=issuer
        )
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img_buffer = BytesIO()
        img.save(img_buffer, format='PNG')
        return img_buffer.getvalue()
    
    @staticmethod
    def verify_totp(secret: str, token: str) -> bool:
        """Verify TOTP token."""
        totp = pyotp.TOTP(secret)
        return totp.verify(token, valid_window=1)  # Allow 30-second window

# Usage in Flask app
@app.route('/setup-mfa', methods=['POST'])
@login_required
def setup_mfa():
    user = current_user
    if not user.mfa_secret:
        user.mfa_secret = MFAManager.generate_secret()
        db.session.commit()
    
    qr_code = MFAManager.generate_qr_code(user.email, user.mfa_secret)
    return send_file(BytesIO(qr_code), mimetype='image/png')

@app.route('/verify-mfa', methods=['POST'])
@login_required
def verify_mfa():
    token = request.json.get('token')
    user = current_user
    
    if MFAManager.verify_totp(user.mfa_secret, token):
        user.mfa_enabled = True
        db.session.commit()
        return jsonify({'success': True})
    
    return jsonify({'error': 'Invalid token'}), 400
```

### JWT Security
```javascript
const jwt = require('jsonwebtoken');
const crypto = require('crypto');

class JWTManager {
    constructor() {
        // Use strong, randomly generated secrets
        this.accessTokenSecret = process.env.JWT_ACCESS_SECRET;
        this.refreshTokenSecret = process.env.JWT_REFRESH_SECRET;
        
        if (!this.accessTokenSecret || !this.refreshTokenSecret) {
            throw new Error('JWT secrets must be set in environment variables');
        }
    }
    
    generateTokens(user) {
        const payload = {
            userId: user.id,
            email: user.email,
            roles: user.roles
        };
        
        // Short-lived access token (15 minutes)
        const accessToken = jwt.sign(payload, this.accessTokenSecret, {
            expiresIn: '15m',
            issuer: 'myapp.com',
            audience: 'myapp-users'
        });
        
        // Longer-lived refresh token (7 days)
        const refreshToken = jwt.sign(
            { userId: user.id, tokenId: crypto.randomUUID() },
            this.refreshTokenSecret,
            { expiresIn: '7d' }
        );
        
        return { accessToken, refreshToken };
    }
    
    verifyAccessToken(token) {
        try {
            return jwt.verify(token, this.accessTokenSecret, {
                issuer: 'myapp.com',
                audience: 'myapp-users'
            });
        } catch (error) {
            throw new Error('Invalid access token');
        }
    }
    
    verifyRefreshToken(token) {
        try {
            return jwt.verify(token, this.refreshTokenSecret);
        } catch (error) {
            throw new Error('Invalid refresh token');
        }
    }
}

// Middleware for token validation
function authenticateToken(req, res, next) {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1]; // Bearer TOKEN
    
    if (!token) {
        return res.status(401).json({ error: 'Access token required' });
    }
    
    try {
        const decoded = jwtManager.verifyAccessToken(token);
        req.user = decoded;
        next();
    } catch (error) {
        return res.status(403).json({ error: 'Invalid or expired token' });
    }
}
```

## Secure Communication (HTTPS/TLS) {#https}

### TLS Configuration
```nginx
# Nginx HTTPS configuration
server {
    listen 443 ssl http2;
    server_name example.com;
    
    # SSL certificate files
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    # Modern TLS configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    # HSTS (HTTP Strict Transport Security)
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
    
    # Perfect Forward Secrecy
    ssl_dhparam /path/to/dhparam.pem;
    
    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /path/to/chain.crt;
    
    # Security headers
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

### Certificate Management
```bash
# Generate Let's Encrypt certificate
certbot --nginx -d example.com -d www.example.com

# Auto-renewal setup
echo "0 0,12 * * * root certbot renew --quiet" | sudo tee -a /etc/crontab

# Custom certificate generation (for development)
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

## Input Validation and Sanitization {#validation}

### Server-Side Validation
```javascript
const validator = require('validator');
const xss = require('xss');

class InputValidator {
    static validateEmail(email) {
        if (!email || typeof email !== 'string') {
            throw new Error('Email is required and must be a string');
        }
        
        if (!validator.isEmail(email)) {
            throw new Error('Invalid email format');
        }
        
        if (email.length > 254) {
            throw new Error('Email too long');
        }
        
        return validator.normalizeEmail(email);
    }
    
    static validatePassword(password) {
        if (!password || typeof password !== 'string') {
            throw new Error('Password is required and must be a string');
        }
        
        if (password.length < 12 || password.length > 128) {
            throw new Error('Password must be between 12 and 128 characters');
        }
        
        const hasUpper = /[A-Z]/.test(password);
        const hasLower = /[a-z]/.test(password);
        const hasNumber = /\d/.test(password);
        const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);
        
        if (!hasUpper || !hasLower || !hasNumber || !hasSpecial) {
            throw new Error('Password must contain uppercase, lowercase, number, and special character');
        }
        
        return password;
    }
    
    static sanitizeHTML(input) {
        if (typeof input !== 'string') return '';
        
        return xss(input, {
            whiteList: {
                p: [],
                br: [],
                strong: [],
                em: [],
                b: [],
                i: []
            },
            stripIgnoreTag: true,
            stripIgnoreTagBody: ['script']
        });
    }
    
    static validateInteger(input, min = null, max = null) {
        const num = parseInt(input, 10);
        
        if (isNaN(num)) {
            throw new Error('Invalid number format');
        }
        
        if (min !== null && num < min) {
            throw new Error(`Number must be at least ${min}`);
        }
        
        if (max !== null && num > max) {
            throw new Error(`Number must be at most ${max}`);
        }
        
        return num;
    }
}

// Express middleware for input validation
function validateUserInput(req, res, next) {
    try {
        if (req.body.email) {
            req.body.email = InputValidator.validateEmail(req.body.email);
        }
        
        if (req.body.password) {
            req.body.password = InputValidator.validatePassword(req.body.password);
        }
        
        if (req.body.comment) {
            req.body.comment = InputValidator.sanitizeHTML(req.body.comment);
        }
        
        next();
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
}
```

### File Upload Security
```javascript
const multer = require('multer');
const path = require('path');
const crypto = require('crypto');

// Secure file upload configuration
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'uploads/');
    },
    filename: (req, file, cb) => {
        // Generate secure filename
        const uniqueSuffix = crypto.randomBytes(16).toString('hex');
        const ext = path.extname(file.originalname);
        cb(null, `${uniqueSuffix}${ext}`);
    }
});

const fileFilter = (req, file, cb) => {
    // Whitelist allowed file types
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf'];
    
    if (allowedTypes.includes(file.mimetype)) {
        cb(null, true);
    } else {
        cb(new Error('Invalid file type'), false);
    }
};

const upload = multer({
    storage: storage,
    limits: {
        fileSize: 5 * 1024 * 1024, // 5MB limit
        files: 5 // Maximum 5 files
    },
    fileFilter: fileFilter
});

// Additional file validation
function validateUploadedFile(req, res, next) {
    if (!req.file) {
        return next();
    }
    
    const file = req.file;
    
    // Verify file extension matches MIME type
    const allowedExtensions = {
        'image/jpeg': ['.jpg', '.jpeg'],
        'image/png': ['.png'],
        'image/gif': ['.gif'],
        'application/pdf': ['.pdf']
    };
    
    const ext = path.extname(file.originalname).toLowerCase();
    const allowedExts = allowedExtensions[file.mimetype];
    
    if (!allowedExts || !allowedExts.includes(ext)) {
        return res.status(400).json({ error: 'File extension does not match MIME type' });
    }
    
    next();
}
```

## Session Management {#sessions}

### Secure Session Configuration
```javascript
const session = require('express-session');
const MongoStore = require('connect-mongo');
const crypto = require('crypto');

// Secure session configuration
app.use(session({
    secret: process.env.SESSION_SECRET, // Strong, random secret
    name: 'sessionId', // Change default session name
    resave: false,
    saveUninitialized: false,
    
    cookie: {
        secure: process.env.NODE_ENV === 'production', // HTTPS only in production
        httpOnly: true, // Prevent XSS
        maxAge: 1000 * 60 * 60 * 24, // 24 hours
        sameSite: 'strict' // CSRF protection
    },
    
    store: MongoStore.create({
        mongoUrl: process.env.MONGODB_URI,
        touchAfter: 24 * 3600 // Lazy session update
    })
}));

// Session security middleware
function sessionSecurity(req, res, next) {
    // Regenerate session ID on login
    if (req.body.action === 'login' && req.user) {
        req.session.regenerate((err) => {
            if (err) {
                return next(err);
            }
            req.session.userId = req.user.id;
            next();
        });
    } else {
        next();
    }
}

// Session timeout handling
function checkSessionTimeout(req, res, next) {
    if (req.session && req.session.lastActivity) {
        const timeout = 30 * 60 * 1000; // 30 minutes
        const now = Date.now();
        
        if (now - req.session.lastActivity > timeout) {
            req.session.destroy((err) => {
                if (err) console.error('Session destruction error:', err);
                return res.status(401).json({ error: 'Session expired' });
            });
            return;
        }
    }
    
    if (req.session) {
        req.session.lastActivity = Date.now();
    }
    
    next();
}
```

## Security Headers and Content Security Policy {#headers}

### Comprehensive Security Headers
```javascript
const helmet = require('helmet');

// Helmet configuration for security headers
app.use(helmet({
    // Content Security Policy
    contentSecurityPolicy: {
        directives: {
            defaultSrc: ["'self'"],
            styleSrc: ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
            fontSrc: ["'self'", "https://fonts.gstatic.com"],
            scriptSrc: ["'self'", "https://cdnjs.cloudflare.com"],
            imgSrc: ["'self'", "data:", "https:"],
            connectSrc: ["'self'", "https://api.example.com"],
            mediaSrc: ["'self'"],
            objectSrc: ["'none'"],
            childSrc: ["'none'"],
            workerSrc: ["'self'"],
            frameSrc: ["'none'"],
            formAction: ["'self'"],
            upgradeInsecureRequests: []
        },
        reportOnly: false
    },
    
    // HTTP Strict Transport Security
    hsts: {
        maxAge: 31536000, // 1 year
        includeSubDomains: true,
        preload: true
    },
    
    // X-Frame-Options
    frameguard: {
        action: 'deny'
    },
    
    // X-Content-Type-Options
    noSniff: true,
    
    // X-XSS-Protection
    xssFilter: true,
    
    // Referrer Policy
    referrerPolicy: {
        policy: 'strict-origin-when-cross-origin'
    },
    
    // Permissions Policy
    permissionsPolicy: {
        features: {
            geolocation: ["'none'"],
            microphone: ["'none'"],
            camera: ["'none'"],
            payment: ["'none'"],
            usb: ["'none'"]
        }
    }
}));

// Custom security headers
app.use((req, res, next) => {
    // Feature Policy (deprecated but still used by some browsers)
    res.setHeader('Feature-Policy', "geolocation 'none'; microphone 'none'; camera 'none'");
    
    // Server header removal
    res.removeHeader('X-Powered-By');
    
    // Custom security header
    res.setHeader('X-Custom-Security', 'enabled');
    
    next();
});
```

### Content Security Policy Implementation
```html
<!-- Inline CSP (fallback) -->
<meta http-equiv="Content-Security-Policy" content="
    default-src 'self';
    script-src 'self' 'nonce-{{nonce}}' https://cdnjs.cloudflare.com;
    style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
    font-src 'self' https://fonts.gstatic.com;
    img-src 'self' data: https:;
    connect-src 'self' https://api.example.com;
    media-src 'self';
    object-src 'none';
    child-src 'none';
    worker-src 'self';
    frame-src 'none';
    form-action 'self';
    upgrade-insecure-requests;
">

<!-- Nonce-based script execution -->
<script nonce="{{nonce}}">
    // Safe inline script with nonce
    console.log('This script is allowed');
</script>
```

## Secure Development Practices {#practices}

### Security Code Review Checklist
```markdown
## Security Code Review Checklist

### Authentication & Authorization
- [ ] Password hashing using bcrypt/scrypt/Argon2
- [ ] Strong password requirements enforced
- [ ] Account lockout mechanisms implemented
- [ ] Multi-factor authentication available
- [ ] Proper session management
- [ ] JWT tokens properly validated
- [ ] Authorization checks on all endpoints
- [ ] Principle of least privilege applied

### Input Validation
- [ ] All user inputs validated server-side
- [ ] Parameterized queries used (no SQL injection)
- [ ] HTML output properly escaped
- [ ] File uploads validated and restricted
- [ ] URL parameters validated
- [ ] JSON input validated against schema

### Data Protection
- [ ] Sensitive data encrypted at rest
- [ ] TLS/HTTPS enforced for data in transit
- [ ] Secrets stored securely (not in code)
- [ ] Database credentials protected
- [ ] API keys managed securely
- [ ] Personal data handling complies with GDPR/CCPA

### Error Handling
- [ ] Generic error messages for user-facing errors
- [ ] Detailed errors logged securely
- [ ] No sensitive information in error messages
- [ ] Proper exception handling implemented
- [ ] Security events logged and monitored

### Dependencies
- [ ] Dependencies regularly updated
- [ ] Vulnerability scanning performed
- [ ] No known vulnerable packages used
- [ ] Dependency integrity verified
```

### Environment Configuration
```bash
# .env file for development (never commit to repo)
NODE_ENV=development
DATABASE_URL=postgresql://user:password@localhost:5432/myapp_dev
SESSION_SECRET=your-super-secret-session-key-here
JWT_ACCESS_SECRET=your-jwt-access-secret-here
JWT_REFRESH_SECRET=your-jwt-refresh-secret-here
ENCRYPTION_KEY=your-32-character-encryption-key-here

# Production environment variables (set in deployment platform)
NODE_ENV=production
DATABASE_URL=${DATABASE_URL}
SESSION_SECRET=${SESSION_SECRET}
JWT_ACCESS_SECRET=${JWT_ACCESS_SECRET}
JWT_REFRESH_SECRET=${JWT_REFRESH_SECRET}
ENCRYPTION_KEY=${ENCRYPTION_KEY}
```

### Secrets Management
```javascript
// Using Azure Key Vault
const { DefaultAzureCredential } = require('@azure/identity');
const { SecretClient } = require('@azure/keyvault-secrets');

class SecretsManager {
    constructor() {
        const credential = new DefaultAzureCredential();
        this.client = new SecretClient(
            process.env.AZURE_KEYVAULT_URL,
            credential
        );
    }
    
    async getSecret(secretName) {
        try {
            const secret = await this.client.getSecret(secretName);
            return secret.value;
        } catch (error) {
            console.error(`Failed to retrieve secret ${secretName}:`, error);
            throw new Error('Failed to retrieve secret');
        }
    }
}

// Usage
const secretsManager = new SecretsManager();
const dbPassword = await secretsManager.getSecret('database-password');
```

## Security Testing and Monitoring {#testing}

### Automated Security Testing
```javascript
// Security testing with Jest and Supertest
const request = require('supertest');
const app = require('../app');

describe('Security Tests', () => {
    test('should prevent SQL injection', async () => {
        const maliciousInput = "'; DROP TABLE users; --";
        
        const response = await request(app)
            .get(`/api/users/${maliciousInput}`)
            .expect(400);
        
        expect(response.body.error).toContain('Invalid input');
    });
    
    test('should prevent XSS in comments', async () => {
        const xssPayload = '<script>alert("XSS")</script>';
        
        const response = await request(app)
            .post('/api/comments')
            .send({ content: xssPayload })
            .expect(201);
        
        expect(response.body.content).not.toContain('<script>');
        expect(response.body.content).toContain('&lt;script&gt;');
    });
    
    test('should require CSRF token for state-changing operations', async () => {
        await request(app)
            .post('/api/transfer-money')
            .send({ amount: 1000, to: 'attacker' })
            .expect(403);
    });
    
    test('should enforce rate limiting', async () => {
        const promises = Array(100).fill().map(() =>
            request(app).post('/api/login').send({ email: 'test@test.com', password: 'wrong' })
        );
        
        const responses = await Promise.all(promises);
        const tooManyRequests = responses.filter(r => r.status === 429);
        
        expect(tooManyRequests.length).toBeGreaterThan(0);
    });
});
```

### Security Monitoring
```javascript
const winston = require('winston');

// Security event logger
const securityLogger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [
        new winston.transports.File({ filename: 'security.log' }),
        new winston.transports.Console()
    ]
});

// Security middleware for monitoring
function securityMonitoring(req, res, next) {
    // Log suspicious activities
    const suspiciousPatterns = [
        /\b(union|select|insert|delete|drop|exec|script)\b/i,
        /<script|javascript:|vbscript:|onload|onerror/i,
        /\.\.\//,
        /\/etc\/passwd|\/proc\/|\/sys\//
    ];
    
    const userInput = JSON.stringify({
        url: req.url,
        body: req.body,
        query: req.query,
        headers: req.headers
    });
    
    suspiciousPatterns.forEach(pattern => {
        if (pattern.test(userInput)) {
            securityLogger.warn('Suspicious activity detected', {
                pattern: pattern.toString(),
                ip: req.ip,
                userAgent: req.get('User-Agent'),
                url: req.url,
                input: userInput
            });
        }
    });
    
    // Log failed authentication attempts
    if (req.url.includes('/login') && res.statusCode === 401) {
        securityLogger.warn('Failed login attempt', {
            ip: req.ip,
            userAgent: req.get('User-Agent'),
            email: req.body.email
        });
    }
    
    next();
}

app.use(securityMonitoring);
```

This comprehensive web security guide covers the fundamental aspects of securing web applications. Security is an ongoing process that requires constant vigilance, regular updates, and continuous learning about new threats and vulnerabilities. Always stay informed about the latest security best practices and update your applications accordingly.

Remember: Security is not a feature you add at the end – it must be built into every aspect of your application from the ground up.''',
            'category': 'Security',
            'tags': 'security,web-security,vulnerabilities,authentication',
        },
        {
            'title': 'Node.js Performance Optimization',
            'content': '''# Node.js Performance Optimization: Complete Guide

## Table of Contents
1. [Performance Fundamentals](#fundamentals)
2. [Event Loop Optimization](#event-loop)
3. [Memory Management](#memory)
4. [Database Optimization](#database)
5. [Caching Strategies](#caching)
6. [HTTP and Network Optimization](#networking)
7. [CPU-Intensive Tasks](#cpu-tasks)
8. [Monitoring and Profiling](#monitoring)
9. [Deployment Optimization](#deployment)
10. [Best Practices Summary](#best-practices)

## Performance Fundamentals {#fundamentals}

Node.js performance optimization requires understanding the event-driven, non-blocking I/O model and identifying bottlenecks in your application.

### Performance Metrics
```javascript
const performance = require('perf_hooks').performance;

// Timing operations
function timeOperation(name, operation) {
    const start = performance.now();
    const result = operation();
    const end = performance.now();
    console.log(`${name} took ${(end - start).toFixed(2)} milliseconds`);
    return result;
}

// Memory usage monitoring
function getMemoryUsage() {
    const usage = process.memoryUsage();
    return {
        rss: Math.round(usage.rss / 1024 / 1024) + ' MB',
        heapTotal: Math.round(usage.heapTotal / 1024 / 1024) + ' MB',
        heapUsed: Math.round(usage.heapUsed / 1024 / 1024) + ' MB',
        external: Math.round(usage.external / 1024 / 1024) + ' MB'
    };
}

// CPU usage monitoring
function getCPUUsage() {
    const usage = process.cpuUsage();
    return {
        user: usage.user / 1000, // Convert to milliseconds
        system: usage.system / 1000
    };
}

// Performance monitoring middleware
function performanceMiddleware(req, res, next) {
    const start = performance.now();
    const startUsage = process.cpuUsage();
    
    res.on('finish', () => {
        const duration = performance.now() - start;
        const cpuUsage = process.cpuUsage(startUsage);
        
        console.log({
            method: req.method,
            url: req.url,
            statusCode: res.statusCode,
            duration: `${duration.toFixed(2)}ms`,
            cpuUser: `${(cpuUsage.user / 1000).toFixed(2)}ms`,
            cpuSystem: `${(cpuUsage.system / 1000).toFixed(2)}ms`,
            memory: getMemoryUsage()
        });
    });
    
    next();
}
```

## Event Loop Optimization {#event-loop}

### Understanding the Event Loop
```javascript
// Avoid blocking the event loop
function badSyncOperation(data) {
    // BAD: Synchronous operation that blocks the event loop
    let result = 0;
    for (let i = 0; i < 1000000000; i++) {
        result += i;
    }
    return result;
}

function goodAsyncOperation(data, callback) {
    // GOOD: Break work into chunks
    let result = 0;
    let i = 0;
    const batchSize = 1000000;
    
    function processChunk() {
        const end = Math.min(i + batchSize, 1000000000);
        
        for (; i < end; i++) {
            result += i;
        }
        
        if (i < 1000000000) {
            // Continue in next tick
            setImmediate(processChunk);
        } else {
            callback(null, result);
        }
    }
    
    processChunk();
}

// Using async/await for better control
async function processDataAsync(data) {
    return new Promise((resolve) => {
        let result = 0;
        let i = 0;
        const batchSize = 1000000;
        
        function processChunk() {
            const end = Math.min(i + batchSize, data.length);
            
            for (; i < end; i++) {
                result += data[i];
            }
            
            if (i < data.length) {
                setImmediate(processChunk);
            } else {
                resolve(result);
            }
        }
        
        processChunk();
    });
}

// Worker threads for CPU-intensive tasks
const { Worker, isMainThread, parentPort } = require('worker_threads');

if (isMainThread) {
    // Main thread
    function heavyComputationWithWorker(data) {
        return new Promise((resolve, reject) => {
            const worker = new Worker(__filename);
            worker.postMessage(data);
            
            worker.on('message', resolve);
            worker.on('error', reject);
            worker.on('exit', (code) => {
                if (code !== 0) {
                    reject(new Error(`Worker stopped with exit code ${code}`));
                }
            });
        });
    }
} else {
    // Worker thread
    parentPort.on('message', (data) => {
        // Perform heavy computation
        let result = 0;
        for (let i = 0; i < data; i++) {
            result += Math.sqrt(i);
        }
        parentPort.postMessage(result);
    });
}

// Stream processing for large datasets
const { Transform } = require('stream');

class DataProcessor extends Transform {
    constructor(options = {}) {
        super({ objectMode: true, ...options });
        this.batchSize = options.batchSize || 100;
        this.batch = [];
    }
    
    _transform(chunk, encoding, callback) {
        this.batch.push(chunk);
        
        if (this.batch.length >= this.batchSize) {
            this.processBatch();
        }
        
        callback();
    }
    
    _flush(callback) {
        if (this.batch.length > 0) {
            this.processBatch();
        }
        callback();
    }
    
    processBatch() {
        const processedBatch = this.batch.map(item => ({
            ...item,
            processed: true,
            timestamp: Date.now()
        }));
        
        processedBatch.forEach(item => this.push(item));
        this.batch = [];
    }
}
```

## Memory Management {#memory}

### Memory Leaks Prevention
```javascript
// Avoiding memory leaks
class MemoryEfficientClass {
    constructor() {
        this.data = new Map();
        this.timers = new Set();
        this.listeners = new Map();
    }
    
    addData(key, value) {
        // Use WeakMap for objects that can be garbage collected
        if (typeof value === 'object') {
            if (!this.weakData) {
                this.weakData = new WeakMap();
            }
            this.weakData.set(value, key);
        } else {
            this.data.set(key, value);
        }
    }
    
    addTimer(interval, callback) {
        const timer = setInterval(callback, interval);
        this.timers.add(timer);
        return timer;
    }
    
    addListener(emitter, event, callback) {
        emitter.on(event, callback);
        
        if (!this.listeners.has(emitter)) {
            this.listeners.set(emitter, new Map());
        }
        this.listeners.get(emitter).set(event, callback);
    }
    
    cleanup() {
        // Clear all timers
        this.timers.forEach(timer => clearInterval(timer));
        this.timers.clear();
        
        // Remove all listeners
        this.listeners.forEach((events, emitter) => {
            events.forEach((callback, event) => {
                emitter.removeListener(event, callback);
            });
        });
        this.listeners.clear();
        
        // Clear data
        this.data.clear();
    }
}

// Object pooling to reduce GC pressure
class ObjectPool {
    constructor(createFn, resetFn, maxSize = 100) {
        this.createFn = createFn;
        this.resetFn = resetFn;
        this.pool = [];
        this.maxSize = maxSize;
    }
    
    acquire() {
        if (this.pool.length > 0) {
            return this.pool.pop();
        }
        return this.createFn();
    }
    
    release(obj) {
        if (this.pool.length < this.maxSize) {
            this.resetFn(obj);
            this.pool.push(obj);
        }
    }
}

// Example: Buffer pool for network operations
const bufferPool = new ObjectPool(
    () => Buffer.allocUnsafe(8192),
    (buffer) => buffer.fill(0),
    50
);

function processNetworkData(data) {
    const buffer = bufferPool.acquire();
    try {
        // Use buffer for processing
        data.copy(buffer);
        return processBuffer(buffer);
    } finally {
        bufferPool.release(buffer);
    }
}

// Memory-efficient data structures
class CircularBuffer {
    constructor(size) {
        this.buffer = new Array(size);
        this.size = size;
        this.head = 0;
        this.tail = 0;
        this.length = 0;
    }
    
    push(item) {
        this.buffer[this.tail] = item;
        this.tail = (this.tail + 1) % this.size;
        
        if (this.length < this.size) {
            this.length++;
        } else {
            this.head = (this.head + 1) % this.size;
        }
    }
    
    pop() {
        if (this.length === 0) return undefined;
        
        this.tail = (this.tail - 1 + this.size) % this.size;
        const item = this.buffer[this.tail];
        this.buffer[this.tail] = undefined;
        this.length--;
        
        return item;
    }
    
    shift() {
        if (this.length === 0) return undefined;
        
        const item = this.buffer[this.head];
        this.buffer[this.head] = undefined;
        this.head = (this.head + 1) % this.size;
        this.length--;
        
        return item;
    }
}
```

## Database Optimization {#database}

### Connection Pooling
```javascript
const { Pool } = require('pg');

// Optimized PostgreSQL connection pool
const pool = new Pool({
    host: process.env.DB_HOST,
    port: process.env.DB_PORT,
    database: process.env.DB_NAME,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    
    // Pool configuration
    max: 20,                    // Maximum number of connections
    idleTimeoutMillis: 30000,   // Close idle connections after 30s
    connectionTimeoutMillis: 2000, // Return error after 2s if can't connect
    maxUses: 7500,              // Close connection after 7500 uses
    
    // Connection settings
    keepAlive: true,
    keepAliveInitialDelayMillis: 10000,
    
    // Query timeout
    query_timeout: 20000,
    
    // SSL configuration
    ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false
});

// Optimized query functions
class DatabaseManager {
    constructor(pool) {
        this.pool = pool;
        this.queryCache = new Map();
    }
    
    async query(text, params = []) {
        const start = Date.now();
        try {
            const result = await this.pool.query(text, params);
            const duration = Date.now() - start;
            
            console.log('Query executed', {
                text: text.substring(0, 100),
                duration: `${duration}ms`,
                rows: result.rowCount
            });
            
            return result;
        } catch (error) {
            console.error('Query error:', error);
            throw error;
        }
    }
    
    // Prepared statements for frequently used queries
    async prepareQuery(name, text) {
        this.queryCache.set(name, text);
    }
    
    async executePrepared(name, params = []) {
        const text = this.queryCache.get(name);
        if (!text) {
            throw new Error(`Prepared query '${name}' not found`);
        }
        
        return this.query(text, params);
    }
    
    // Batch operations
    async batchInsert(table, columns, data) {
        if (data.length === 0) return;
        
        const valueStrings = data.map((_, index) => {
            const start = index * columns.length;
            const placeholders = columns.map((_, colIndex) => 
                `$${start + colIndex + 1}`
            ).join(', ');
            return `(${placeholders})`;
        }).join(', ');
        
        const query = `
            INSERT INTO ${table} (${columns.join(', ')})
            VALUES ${valueStrings}
        `;
        
        const flatValues = data.flat();
        return this.query(query, flatValues);
    }
    
    // Transaction management
    async withTransaction(callback) {
        const client = await this.pool.connect();
        
        try {
            await client.query('BEGIN');
            const result = await callback(client);
            await client.query('COMMIT');
            return result;
        } catch (error) {
            await client.query('ROLLBACK');
            throw error;
        } finally {
            client.release();
        }
    }
    
    // Connection health check
    async healthCheck() {
        try {
            const result = await this.query('SELECT 1 as healthy');
            return result.rows[0].healthy === 1;
        } catch (error) {
            return false;
        }
    }
}

// Query optimization examples
const optimizedQueries = {
    // Use indexes effectively
    getUserByEmail: `
        SELECT id, name, email, created_at
        FROM users
        WHERE email = $1
        LIMIT 1
    `,
    
    // Pagination with OFFSET can be slow, use cursor-based pagination
    getUsersPaginated: `
        SELECT id, name, email, created_at
        FROM users
        WHERE id > $1
        ORDER BY id
        LIMIT $2
    `,
    
    // Join optimization
    getUsersWithPosts: `
        SELECT 
            u.id,
            u.name,
            u.email,
            COUNT(p.id) as post_count
        FROM users u
        LEFT JOIN posts p ON u.id = p.user_id
        WHERE u.active = true
        GROUP BY u.id, u.name, u.email
        HAVING COUNT(p.id) > 0
        ORDER BY post_count DESC
        LIMIT $1
    `,
    
    // Batch update
    updateUserLastSeen: `
        UPDATE users
        SET last_seen = NOW()
        WHERE id = ANY($1::int[])
    `
};
```

## Caching Strategies {#caching}

### Multi-level Caching
```javascript
const Redis = require('ioredis');
const LRU = require('lru-cache');

class CacheManager {
    constructor() {
        // Level 1: In-memory cache (fastest)
        this.memoryCache = new LRU({
            max: 1000,           // Maximum items
            ttl: 5 * 60 * 1000,  // 5 minutes TTL
            updateAgeOnGet: true
        });
        
        // Level 2: Redis cache (shared across instances)
        this.redisCache = new Redis({
            host: process.env.REDIS_HOST || 'localhost',
            port: process.env.REDIS_PORT || 6379,
            password: process.env.REDIS_PASSWORD,
            db: 0,
            retryDelayOnFailover: 100,
            maxRetriesPerRequest: 3,
            lazyConnect: true,
            
            // Connection pool
            family: 4,
            keepAlive: true,
            
            // Cluster configuration if using Redis Cluster
            // enableOfflineQueue: false
        });
        
        this.defaultTTL = 300; // 5 minutes
    }
    
    // Get with fallback strategy
    async get(key, fallbackFn = null, ttl = this.defaultTTL) {
        // Try memory cache first
        let value = this.memoryCache.get(key);
        if (value !== undefined) {
            return JSON.parse(value);
        }
        
        // Try Redis cache
        try {
            value = await this.redisCache.get(key);
            if (value) {
                // Store in memory cache for faster future access
                this.memoryCache.set(key, value);
                return JSON.parse(value);
            }
        } catch (error) {
            console.error('Redis get error:', error);
        }
        
        // Use fallback function if provided
        if (fallbackFn) {
            const data = await fallbackFn();
            await this.set(key, data, ttl);
            return data;
        }
        
        return null;
    }
    
    // Set in both caches
    async set(key, value, ttl = this.defaultTTL) {
        const serialized = JSON.stringify(value);
        
        // Set in memory cache
        this.memoryCache.set(key, serialized);
        
        // Set in Redis cache
        try {
            await this.redisCache.setex(key, ttl, serialized);
        } catch (error) {
            console.error('Redis set error:', error);
        }
    }
    
    // Delete from both caches
    async delete(key) {
        this.memoryCache.delete(key);
        
        try {
            await this.redisCache.del(key);
        } catch (error) {
            console.error('Redis delete error:', error);
        }
    }
    
    // Cache invalidation patterns
    async invalidatePattern(pattern) {
        // Clear memory cache (simple approach - clear all)
        this.memoryCache.clear();
        
        // Clear Redis keys matching pattern
        try {
            const keys = await this.redisCache.keys(pattern);
            if (keys.length > 0) {
                await this.redisCache.del(...keys);
            }
        } catch (error) {
            console.error('Redis pattern delete error:', error);
        }
    }
    
    // Cache warming
    async warmCache(warmingFunctions) {
        for (const [key, fn] of Object.entries(warmingFunctions)) {
            try {
                const data = await fn();
                await this.set(key, data);
                console.log(`Cache warmed for key: ${key}`);
            } catch (error) {
                console.error(`Cache warming failed for key ${key}:`, error);
            }
        }
    }
}

// HTTP response caching middleware
function createCacheMiddleware(cacheManager) {
    return function cacheMiddleware(options = {}) {
        return async (req, res, next) => {
            // Skip caching for non-GET requests
            if (req.method !== 'GET') {
                return next();
            }
            
            // Create cache key
            const cacheKey = options.keyGenerator ? 
                options.keyGenerator(req) : 
                `http:${req.originalUrl}`;
            
            try {
                // Try to get cached response
                const cached = await cacheManager.get(cacheKey);
                if (cached) {
                    res.set(cached.headers);
                    return res.status(cached.status).send(cached.body);
                }
                
                // Capture response
                const originalSend = res.send;
                const originalJson = res.json;
                
                res.send = function(body) {
                    // Cache successful responses
                    if (res.statusCode >= 200 && res.statusCode < 300) {
                        cacheManager.set(cacheKey, {
                            status: res.statusCode,
                            headers: res.getHeaders(),
                            body: body
                        }, options.ttl);
                    }
                    
                    originalSend.call(this, body);
                };
                
                res.json = function(obj) {
                    if (res.statusCode >= 200 && res.statusCode < 300) {
                        cacheManager.set(cacheKey, {
                            status: res.statusCode,
                            headers: res.getHeaders(),
                            body: obj
                        }, options.ttl);
                    }
                    
                    originalJson.call(this, obj);
                };
                
            } catch (error) {
                console.error('Cache middleware error:', error);
            }
            
            next();
        };
    };
}

// Application-level caching strategies
class DataService {
    constructor(cacheManager, dbManager) {
        this.cache = cacheManager;
        this.db = dbManager;
    }
    
    // Read-through cache pattern
    async getUser(userId) {
        return this.cache.get(
            `user:${userId}`,
            async () => {
                const result = await this.db.query(
                    'SELECT * FROM users WHERE id = $1',
                    [userId]
                );
                return result.rows[0];
            },
            300 // 5 minutes TTL
        );
    }
    
    // Write-through cache pattern
    async updateUser(userId, userData) {
        // Update database
        const result = await this.db.query(
            'UPDATE users SET name = $1, email = $2 WHERE id = $3 RETURNING *',
            [userData.name, userData.email, userId]
        );
        
        // Update cache
        const updatedUser = result.rows[0];
        await this.cache.set(`user:${userId}`, updatedUser);
        
        return updatedUser;
    }
    
    // Cache-aside pattern with batch operations
    async getUsersBatch(userIds) {
        const cached = new Map();
        const missingIds = [];
        
        // Check cache for each user
        for (const id of userIds) {
            const user = await this.cache.get(`user:${id}`);
            if (user) {
                cached.set(id, user);
            } else {
                missingIds.push(id);
            }
        }
        
        // Fetch missing users from database
        if (missingIds.length > 0) {
            const result = await this.db.query(
                'SELECT * FROM users WHERE id = ANY($1::int[])',
                [missingIds]
            );
            
            // Cache the fetched users
            for (const user of result.rows) {
                cached.set(user.id, user);
                await this.cache.set(`user:${user.id}`, user);
            }
        }
        
        return Array.from(cached.values());
    }
}
```

This comprehensive Node.js performance optimization guide covers the essential techniques for building high-performance applications. Remember that premature optimization is the root of all evil - always profile first, identify actual bottlenecks, then apply the appropriate optimization techniques.''',
            'category': 'Web Development',
            'tags': 'nodejs,performance,optimization,javascript',
        },
        {
            'title': 'Kubernetes Basics',
            'content': '''# Kubernetes Basics: Complete Container Orchestration Guide

## Table of Contents
1. [Introduction to Kubernetes](#introduction)
2. [Core Concepts and Architecture](#architecture)
3. [Pods: The Basic Unit](#pods)
4. [Services and Networking](#services)
5. [Deployments and ReplicaSets](#deployments)
6. [ConfigMaps and Secrets](#config)
7. [Persistent Volumes](#storage)
8. [Namespaces and Resource Management](#namespaces)
9. [Monitoring and Debugging](#monitoring)
10. [Best Practices](#best-practices)

## Introduction to Kubernetes {#introduction}

Kubernetes (K8s) is an open-source container orchestration platform that automates the deployment, scaling, and management of containerized applications. Originally developed by Google, it's now maintained by the Cloud Native Computing Foundation (CNCF).

### Why Kubernetes?
- **Automatic scaling**: Scale applications up or down based on demand
- **Self-healing**: Automatically restart failed containers and reschedule them
- **Service discovery**: Built-in load balancing and service discovery
- **Rolling updates**: Deploy new versions with zero downtime
- **Resource optimization**: Efficient utilization of cluster resources

### Key Benefits
```yaml
# High availability through redundancy
# Horizontal scaling capabilities  
# Declarative configuration
# Platform independence
# Extensive ecosystem
```

## Core Concepts and Architecture {#architecture}

### Cluster Architecture
A Kubernetes cluster consists of a control plane and worker nodes:

```
┌─────────────────────────────────────────────────────────┐
│                    Control Plane                        │
├─────────────────┬─────────────────┬─────────────────────┤
│   API Server    │   Controller    │     Scheduler       │
│                 │    Manager      │                     │
├─────────────────┼─────────────────┼─────────────────────┤
│                 │      etcd       │                     │
└─────────────────┴─────────────────┴─────────────────────┘
         │                 │                 │
         └─────────────────┼─────────────────┘
                           │
    ┌─────────────────────────────────────────────┐
    │                Worker Nodes                 │
    ├─────────────┬─────────────┬─────────────────┤
    │   kubelet   │ kube-proxy  │  Container      │
    │             │             │  Runtime        │
    └─────────────┴─────────────┴─────────────────┘
```

### Control Plane Components
```yaml
# API Server: Entry point for all REST commands
# etcd: Distributed key-value store for cluster data
# Controller Manager: Runs controller processes
# Scheduler: Assigns pods to nodes
# Cloud Controller Manager: Interfaces with cloud providers
```

### Node Components
```bash
# kubelet: Agent that runs on each node
# kube-proxy: Network proxy maintaining network rules
# Container Runtime: Docker, containerd, or CRI-O
```

### Essential Objects
```yaml
# Pods: Smallest deployable units
# Services: Network abstraction for pods
# Deployments: Manage application lifecycle
# ConfigMaps: Configuration data
# Secrets: Sensitive data
# PersistentVolumes: Storage abstraction
```

## Pods: The Basic Unit {#pods}

### What is a Pod?
A Pod is the smallest deployable unit in Kubernetes, containing one or more containers that share storage and network.

### Basic Pod Definition
```yaml
# simple-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  labels:
    app: nginx
    environment: development
spec:
  containers:
  - name: nginx
    image: nginx:1.21
    ports:
    - containerPort: 80
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
    env:
    - name: ENVIRONMENT
      value: "development"
    - name: LOG_LEVEL
      value: "info"
  restartPolicy: Always
```

### Multi-Container Pod
```yaml
# multi-container-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-app-pod
spec:
  containers:
  - name: web-app
    image: my-web-app:v1.0
    ports:
    - containerPort: 8080
    volumeMounts:
    - name: shared-data
      mountPath: /var/data
  - name: sidecar-logger
    image: fluentd:v1.14
    volumeMounts:
    - name: shared-data
      mountPath: /var/log
    - name: config
      mountPath: /fluentd/etc
  volumes:
  - name: shared-data
    emptyDir: {}
  - name: config
    configMap:
      name: fluentd-config
```

### Pod Lifecycle Commands
```bash
# Create a pod
kubectl apply -f simple-pod.yaml

# List pods
kubectl get pods
kubectl get pods -o wide  # More details
kubectl get pods --show-labels

# Describe pod
kubectl describe pod nginx-pod

# Get pod logs
kubectl logs nginx-pod
kubectl logs nginx-pod -c nginx  # Specific container

# Execute commands in pod
kubectl exec -it nginx-pod -- /bin/bash
kubectl exec nginx-pod -- ls -la /usr/share/nginx/html

# Port forwarding
kubectl port-forward nginx-pod 8080:80

# Delete pod
kubectl delete pod nginx-pod
kubectl delete -f simple-pod.yaml
```

## Services and Networking {#services}

### Service Types
```yaml
# ClusterIP (default): Internal cluster access only
# NodePort: Exposes service on each node's IP
# LoadBalancer: External load balancer (cloud provider)
# ExternalName: Maps to external service
```

### ClusterIP Service
```yaml
# clusterip-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  type: ClusterIP
  selector:
    app: nginx
  ports:
  - name: http
    port: 80
    targetPort: 80
    protocol: TCP
```

### NodePort Service
```yaml
# nodeport-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-nodeport
spec:
  type: NodePort
  selector:
    app: nginx
  ports:
  - name: http
    port: 80
    targetPort: 80
    nodePort: 30080
```

### LoadBalancer Service
```yaml
# loadbalancer-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-loadbalancer
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
spec:
  type: LoadBalancer
  selector:
    app: nginx
  ports:
  - name: http
    port: 80
    targetPort: 80
```

### Ingress Configuration
```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - myapp.example.com
    secretName: myapp-tls
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 8080
```

### Service Discovery
```bash
# DNS-based service discovery
# Services are accessible via:
# <service-name>.<namespace>.svc.cluster.local

# Environment variables
# Kubernetes automatically creates environment variables for services
```

## Deployments and ReplicaSets {#deployments}

### Deployment Definition
```yaml
# nginx-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
        ports:
        - containerPort: 80
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
```

### Deployment Operations
```bash
# Create deployment
kubectl apply -f nginx-deployment.yaml

# Get deployments
kubectl get deployments
kubectl get deployment nginx-deployment -o yaml

# Scale deployment
kubectl scale deployment nginx-deployment --replicas=5

# Update deployment
kubectl set image deployment/nginx-deployment nginx=nginx:1.22

# Rollout status
kubectl rollout status deployment/nginx-deployment

# Rollout history
kubectl rollout history deployment/nginx-deployment

# Rollback deployment
kubectl rollout undo deployment/nginx-deployment
kubectl rollout undo deployment/nginx-deployment --to-revision=2

# Pause/Resume rollout
kubectl rollout pause deployment/nginx-deployment
kubectl rollout resume deployment/nginx-deployment
```

### Advanced Deployment Strategies
```yaml
# Blue-Green Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: blue
  template:
    metadata:
      labels:
        app: myapp
        version: blue
    spec:
      containers:
      - name: app
        image: myapp:v1.0

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: green
  template:
    metadata:
      labels:
        app: myapp
        version: green
    spec:
      containers:
      - name: app
        image: myapp:v2.0
```

## ConfigMaps and Secrets {#config}

### ConfigMap Examples
```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  # Key-value pairs
  database_host: "postgres.example.com"
  database_port: "5432"
  log_level: "info"
  
  # File content
  nginx.conf: |
    server {
        listen 80;
        server_name localhost;
        
        location / {
            root /usr/share/nginx/html;
            index index.html;
        }
        
        location /api/ {
            proxy_pass http://backend:8080/;
        }
    }
    
  app.properties: |
    spring.datasource.url=jdbc:postgresql://postgres:5432/mydb
    spring.datasource.username=user
    logging.level.org.springframework=INFO
```

### Using ConfigMaps in Pods
```yaml
# pod-with-configmap.yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-pod
spec:
  containers:
  - name: app
    image: myapp:latest
    # Environment variables from ConfigMap
    envFrom:
    - configMapRef:
        name: app-config
    # Specific environment variable
    env:
    - name: DB_HOST
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: database_host
    # Mount as volume
    volumeMounts:
    - name: config-volume
      mountPath: /etc/config
    - name: nginx-config
      mountPath: /etc/nginx/conf.d/default.conf
      subPath: nginx.conf
  volumes:
  - name: config-volume
    configMap:
      name: app-config
  - name: nginx-config
    configMap:
      name: app-config
```

### Secrets Management
```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  # Base64 encoded values
  username: YWRtaW4=  # admin
  password: MWYyZDFlMmU2N2Rm  # secret_password
  api_key: YWJjZGVmZ2hpams=
  
---
# TLS Secret
apiVersion: v1
kind: Secret
metadata:
  name: tls-secret
type: kubernetes.io/tls
data:
  tls.crt: |
    LS0tLS1CRUdJTi... (base64 encoded certificate)
  tls.key: |
    LS0tLS1CRUdJTi... (base64 encoded private key)
```

### Using Secrets in Pods
```yaml
# pod-with-secrets.yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-with-secrets
spec:
  containers:
  - name: app
    image: myapp:latest
    env:
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: app-secrets
          key: password
    - name: API_KEY
      valueFrom:
        secretKeyRef:
          name: app-secrets
          key: api_key
    volumeMounts:
    - name: secret-volume
      mountPath: /etc/secrets
      readOnly: true
  volumes:
  - name: secret-volume
    secret:
      secretName: app-secrets
      defaultMode: 0400
```

### ConfigMap and Secret Commands
```bash
# Create ConfigMap from literal
kubectl create configmap app-config \
  --from-literal=db_host=postgres.example.com \
  --from-literal=db_port=5432

# Create ConfigMap from file
kubectl create configmap nginx-config --from-file=nginx.conf

# Create Secret from literal
kubectl create secret generic app-secrets \
  --from-literal=username=admin \
  --from-literal=password=secret123

# Create TLS Secret
kubectl create secret tls tls-secret \
  --cert=path/to/cert.crt \
  --key=path/to/cert.key

# View ConfigMap/Secret
kubectl get configmap app-config -o yaml
kubectl describe secret app-secrets

# Edit ConfigMap/Secret
kubectl edit configmap app-config
kubectl patch configmap app-config -p '{"data":{"new_key":"new_value"}}'
```

## Persistent Volumes {#storage}

### PersistentVolume Definition
```yaml
# persistent-volume.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-storage
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: fast-ssd
  hostPath:
    path: /data/pv-storage

---
# For cloud environments
apiVersion: v1
kind: PersistentVolume
metadata:
  name: aws-ebs-pv
spec:
  capacity:
    storage: 20Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Delete
  storageClassName: gp3
  awsElasticBlockStore:
    volumeID: vol-1234567890abcdef0
    fsType: ext4
```

### PersistentVolumeClaim
```yaml
# persistent-volume-claim.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: storage-claim
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: fast-ssd
```

### StatefulSet with Persistent Storage
```yaml
# statefulset.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: database
spec:
  serviceName: database-service
  replicas: 3
  selector:
    matchLabels:
      app: database
  template:
    metadata:
      labels:
        app: database
    spec:
      containers:
      - name: postgres
        image: postgres:13
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_DB
          value: myapp
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: db-secrets
              key: username
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-secrets
              key: password
        volumeMounts:
        - name: storage
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: storage
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: fast-ssd
      resources:
        requests:
          storage: 10Gi
```

### Storage Classes
```yaml
# storageclass.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3
  iops: "3000"
  throughput: "125"
allowVolumeExpansion: true
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
```

## Namespaces and Resource Management {#namespaces}

### Namespace Definition
```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    environment: production
    team: backend
---
apiVersion: v1
kind: Namespace
metadata:
  name: development
  labels:
    environment: development
    team: backend
```

### Resource Quotas
```yaml
# resource-quota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: development
spec:
  hard:
    requests.cpu: "4"
    requests.memory: 8Gi
    limits.cpu: "8"
    limits.memory: 16Gi
    pods: "10"
    persistentvolumeclaims: "5"
    services: "5"
    secrets: "10"
    configmaps: "10"
```

### Limit Ranges
```yaml
# limit-range.yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: resource-limits
  namespace: development
spec:
  limits:
  - default:
      memory: "512Mi"
      cpu: "200m"
    defaultRequest:
      memory: "256Mi"
      cpu: "100m"
    type: Container
  - max:
      memory: "2Gi"
      cpu: "1"
    min:
      memory: "128Mi"
      cpu: "50m"
    type: Container
```

### Network Policies
```yaml
# network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress

---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
```

## Monitoring and Debugging {#monitoring}

### Health Checks
```yaml
# deployment-with-probes.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
    spec:
      containers:
      - name: web
        image: myapp:latest
        ports:
        - containerPort: 8080
        # Liveness Probe
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        # Readiness Probe
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        # Startup Probe
        startupProbe:
          httpGet:
            path: /startup
            port: 8080
          initialDelaySeconds: 0
          periodSeconds: 10
          timeoutSeconds: 3
          failureThreshold: 30
```

### Debugging Commands
```bash
# Pod debugging
kubectl get pods -o wide
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl logs <pod-name> -c <container-name>
kubectl logs <pod-name> --previous
kubectl logs -f <pod-name>  # Follow logs

# Execute commands in pods
kubectl exec -it <pod-name> -- /bin/bash
kubectl exec <pod-name> -- ps aux
kubectl exec <pod-name> -- cat /etc/hosts

# Resource usage
kubectl top nodes
kubectl top pods
kubectl top pods --sort-by=cpu
kubectl top pods --sort-by=memory

# Events
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl get events --field-selector type=Warning

# Debug services
kubectl get endpoints
kubectl describe service <service-name>

# Port forwarding for debugging
kubectl port-forward pod/<pod-name> 8080:80
kubectl port-forward service/<service-name> 8080:80

# Copy files to/from pods
kubectl cp <pod-name>:/path/to/file ./local-file
kubectl cp ./local-file <pod-name>:/path/to/file
```

### Monitoring with Prometheus
```yaml
# prometheus-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus
spec:
  replicas: 1
  selector:
    matchLabels:
      app: prometheus
  template:
    metadata:
      labels:
        app: prometheus
    spec:
      containers:
      - name: prometheus
        image: prom/prometheus:latest
        ports:
        - containerPort: 9090
        volumeMounts:
        - name: config
          mountPath: /etc/prometheus
        - name: storage
          mountPath: /prometheus
      volumes:
      - name: config
        configMap:
          name: prometheus-config
      - name: storage
        emptyDir: {}
```

## Best Practices {#best-practices}

### Security Best Practices
```yaml
# security-context.yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    runAsGroup: 1000
    fsGroup: 1000
  containers:
  - name: app
    image: myapp:latest
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
        add:
        - NET_BIND_SERVICE
    volumeMounts:
    - name: tmp
      mountPath: /tmp
    - name: var-run
      mountPath: /var/run
  volumes:
  - name: tmp
    emptyDir: {}
  - name: var-run
    emptyDir: {}
```

### Resource Management
```yaml
# Always specify resource requests and limits
resources:
  requests:
    memory: "256Mi"
    cpu: "100m"
  limits:
    memory: "512Mi"
    cpu: "200m"

# Use Horizontal Pod Autoscaler
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Deployment Best Practices
```bash
# Use labels consistently
app: myapp
version: v1.2.3
environment: production
team: backend

# Implement rolling updates
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0

# Use health checks
# Always define readiness and liveness probes

# Version your images
# Never use :latest tag in production

# Use secrets for sensitive data
# Never hardcode passwords or API keys

# Implement resource quotas
# Set appropriate resource requests and limits

# Use namespaces for isolation
# Separate environments with namespaces
```

### Troubleshooting Checklist
```bash
# 1. Check pod status
kubectl get pods

# 2. Check pod details
kubectl describe pod <pod-name>

# 3. Check logs
kubectl logs <pod-name>

# 4. Check events
kubectl get events

# 5. Check resource usage
kubectl top pods

# 6. Check service endpoints
kubectl get endpoints

# 7. Test connectivity
kubectl exec -it <pod-name> -- nslookup <service-name>

# 8. Check network policies
kubectl get networkpolicies

# 9. Verify RBAC permissions
kubectl auth can-i <verb> <resource>

# 10. Check cluster health
kubectl get nodes
kubectl cluster-info
```

This comprehensive guide covers the fundamental concepts and practical implementations of Kubernetes. As you work with Kubernetes, remember that it's a powerful but complex platform. Start with simple deployments and gradually introduce more advanced features as your understanding grows.

The key to mastering Kubernetes is hands-on practice. Set up a local cluster using minikube or kind, experiment with different configurations, and build real applications to gain practical experience with container orchestration.''',
            'category': 'DevOps',
            'tags': 'kubernetes,k8s,container-orchestration,devops',
        },
        {
            'title': 'REST API Design Principles',
            'content': '''# REST API Design Principles: Building Scalable Web Services

## Table of Contents
1. [Introduction to REST](#introduction)
2. [Core REST Principles](#principles)
3. [HTTP Methods and Status Codes](#http-methods)
4. [URL Design and Resource Naming](#url-design)
5. [Request and Response Structure](#request-response)
6. [Authentication and Authorization](#auth)
7. [Error Handling](#error-handling)
8. [Versioning Strategies](#versioning)
9. [Caching and Performance](#performance)
10. [Security Best Practices](#security)
11. [Documentation and Testing](#documentation)

## Introduction to REST {#introduction}

Representational State Transfer (REST) is an architectural style for designing networked applications, particularly web services. REST was introduced by Roy Fielding in his doctoral dissertation in 2000 and has become the standard for building web APIs.

### What is REST?
REST is not a protocol or standard, but rather a set of architectural principles that define how web standards like HTTP should be used to create web services.

### Benefits of RESTful Design
- **Simplicity**: Easy to understand and implement
- **Scalability**: Stateless nature enables horizontal scaling
- **Flexibility**: Platform and language agnostic
- **Performance**: Leverages HTTP caching mechanisms
- **Visibility**: Clear separation between client and server

### REST vs. Other Paradigms
```javascript
// REST: Resource-oriented
GET /api/users/123
PUT /api/users/123
DELETE /api/users/123

// RPC: Action-oriented
POST /api/getUser
POST /api/updateUser
POST /api/deleteUser

// GraphQL: Query-oriented
POST /graphql
{
  query: "{ user(id: 123) { name, email } }"
}
```

## Core REST Principles {#principles}

### 1. Uniform Interface
The uniform interface constraint defines the interface between clients and servers:

#### Resource Identification
Resources are identified by URIs:
```http
GET /api/v1/users/123
GET /api/v1/orders/456
GET /api/v1/products?category=electronics
```

#### Resource Manipulation through Representations
Resources are manipulated through their representations (JSON, XML, etc.):
```json
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2023-01-15T10:30:00Z"
}
```

#### Self-Descriptive Messages
Each message includes enough information to describe how to process it:
```http
GET /api/v1/users/123 HTTP/1.1
Host: api.example.com
Accept: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 156
Cache-Control: max-age=3600

{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com"
}
```

#### Hypermedia as the Engine of Application State (HATEOAS)
Responses include links to related resources:
```json
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com",
  "_links": {
    "self": { "href": "/api/v1/users/123" },
    "orders": { "href": "/api/v1/users/123/orders" },
    "profile": { "href": "/api/v1/users/123/profile" }
  }
}
```

### 2. Stateless
Each request must contain all information needed to understand and process it:

```javascript
// Bad: Server-side session state
// Server stores user session information

// Good: Stateless with JWT token
const headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
  'Content-Type': 'application/json'
};
```

### 3. Cacheable
Responses must define themselves as cacheable or non-cacheable:

```http
HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: public, max-age=3600
ETag: "abc123"
Last-Modified: Wed, 21 Oct 2023 07:28:00 GMT
```

### 4. Client-Server
Clear separation of concerns between client and server:
- Client handles user interface and user experience
- Server handles data storage and business logic
- They can evolve independently

### 5. Layered System
Architecture can be composed of hierarchical layers:
```
Client → Load Balancer → API Gateway → Authentication Service → Business Logic → Database
```

### 6. Code on Demand (Optional)
Server can extend client functionality by transferring executable code:
```json
{
  "data": { ... },
  "scripts": [
    "/js/validation.js",
    "/js/formatting.js"
  ]
}
```

## HTTP Methods and Status Codes {#http-methods}

### HTTP Methods (Verbs)

#### GET - Retrieve Resources
```http
GET /api/v1/users
GET /api/v1/users/123
GET /api/v1/users/123/orders

Response: 200 OK
{
  "users": [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
  ],
  "total": 2,
  "page": 1,
  "per_page": 10
}
```

#### POST - Create Resources
```http
POST /api/v1/users
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com"
}

Response: 201 Created
Location: /api/v1/users/123
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2023-01-15T10:30:00Z"
}
```

#### PUT - Update/Replace Resources
```http
PUT /api/v1/users/123
Content-Type: application/json

{
  "name": "John Smith",
  "email": "john.smith@example.com"
}

Response: 200 OK
{
  "id": 123,
  "name": "John Smith",
  "email": "john.smith@example.com",
  "updated_at": "2023-01-15T11:30:00Z"
}
```

#### PATCH - Partial Update
```http
PATCH /api/v1/users/123
Content-Type: application/json

{
  "email": "newemail@example.com"
}

Response: 200 OK
{
  "id": 123,
  "name": "John Doe",
  "email": "newemail@example.com",
  "updated_at": "2023-01-15T11:45:00Z"
}
```

#### DELETE - Remove Resources
```http
DELETE /api/v1/users/123

Response: 204 No Content
```

### HTTP Status Codes

#### Success Codes (2xx)
```javascript
// 200 OK - General success
// 201 Created - Resource created successfully
// 202 Accepted - Request accepted for processing
// 204 No Content - Success with no response body
// 206 Partial Content - Partial response (pagination)

const statusCodes = {
  SUCCESS: 200,
  CREATED: 201,
  ACCEPTED: 202,
  NO_CONTENT: 204,
  PARTIAL_CONTENT: 206
};
```

#### Client Error Codes (4xx)
```javascript
// 400 Bad Request - Invalid request syntax
// 401 Unauthorized - Authentication required
// 403 Forbidden - Insufficient permissions
// 404 Not Found - Resource doesn't exist
// 405 Method Not Allowed - HTTP method not supported
// 409 Conflict - Resource conflict
// 422 Unprocessable Entity - Validation errors
// 429 Too Many Requests - Rate limit exceeded

const clientErrors = {
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  METHOD_NOT_ALLOWED: 405,
  CONFLICT: 409,
  UNPROCESSABLE_ENTITY: 422,
  TOO_MANY_REQUESTS: 429
};
```

#### Server Error Codes (5xx)
```javascript
// 500 Internal Server Error - Generic server error
// 502 Bad Gateway - Invalid response from upstream
// 503 Service Unavailable - Server temporarily unavailable
// 504 Gateway Timeout - Upstream timeout

const serverErrors = {
  INTERNAL_SERVER_ERROR: 500,
  BAD_GATEWAY: 502,
  SERVICE_UNAVAILABLE: 503,
  GATEWAY_TIMEOUT: 504
};
```

## URL Design and Resource Naming {#url-design}

### Resource Naming Conventions

#### Use Nouns, Not Verbs
```http
# Good
GET /api/v1/users
POST /api/v1/users
GET /api/v1/orders/123

# Bad
GET /api/v1/getUsers
POST /api/v1/createUser
GET /api/v1/retrieveOrder/123
```

#### Use Plural Nouns for Collections
```http
# Good
GET /api/v1/users
GET /api/v1/products
GET /api/v1/orders

# Bad
GET /api/v1/user
GET /api/v1/product
GET /api/v1/order
```

#### Use Hierarchical Structure for Relationships
```http
# User's orders
GET /api/v1/users/123/orders

# Order's items
GET /api/v1/orders/456/items

# Product reviews
GET /api/v1/products/789/reviews
```

### URL Structure Examples

#### Collection and Resource Operations
```javascript
// Collection operations
const apiEndpoints = {
  // Get all users
  getAllUsers: 'GET /api/v1/users',
  
  // Create new user
  createUser: 'POST /api/v1/users',
  
  // Get specific user
  getUser: 'GET /api/v1/users/:id',
  
  // Update user
  updateUser: 'PUT /api/v1/users/:id',
  
  // Partially update user
  patchUser: 'PATCH /api/v1/users/:id',
  
  // Delete user
  deleteUser: 'DELETE /api/v1/users/:id'
};
```

#### Query Parameters for Filtering and Pagination
```http
# Filtering
GET /api/v1/users?status=active&role=admin
GET /api/v1/products?category=electronics&price_min=100&price_max=500

# Sorting
GET /api/v1/users?sort=name&order=asc
GET /api/v1/products?sort=price,desc&sort=rating,desc

# Pagination
GET /api/v1/users?page=2&per_page=20
GET /api/v1/users?offset=40&limit=20

# Field selection
GET /api/v1/users?fields=id,name,email
GET /api/v1/products?include=category,reviews&exclude=internal_notes
```

#### Search Operations
```http
# Simple search
GET /api/v1/users?q=john

# Advanced search
GET /api/v1/products?search[name]=laptop&search[category]=electronics

# Full-text search
GET /api/v1/articles?query=javascript&highlight=true
```

### Path Parameters vs Query Parameters

#### Path Parameters (Resource Identification)
```javascript
// Path parameters identify specific resources
app.get('/api/v1/users/:userId/orders/:orderId', (req, res) => {
  const { userId, orderId } = req.params;
  // Fetch specific order for specific user
});
```

#### Query Parameters (Resource Modification)
```javascript
// Query parameters modify the response
app.get('/api/v1/users', (req, res) => {
  const { 
    page = 1, 
    per_page = 10, 
    status, 
    sort = 'id',
    order = 'asc' 
  } = req.query;
  // Filter, sort, and paginate users
});
```

## Request and Response Structure {#request-response}

### Request Structure

#### Headers
```http
POST /api/v1/users HTTP/1.1
Host: api.example.com
Content-Type: application/json
Accept: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
User-Agent: MyApp/1.0
X-Request-ID: abc123-def456-ghi789
```

#### Request Body Structure
```json
{
  "data": {
    "type": "user",
    "attributes": {
      "name": "John Doe",
      "email": "john@example.com",
      "preferences": {
        "language": "en",
        "timezone": "UTC"
      }
    }
  }
}
```

### Response Structure

#### Consistent Response Format
```json
{
  "status": "success",
  "data": {
    "id": 123,
    "type": "user",
    "attributes": {
      "name": "John Doe",
      "email": "john@example.com",
      "created_at": "2023-01-15T10:30:00Z"
    }
  },
  "meta": {
    "request_id": "abc123-def456-ghi789",
    "timestamp": "2023-01-15T10:30:00Z"
  }
}
```

#### Collection Response Format
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "type": "user",
      "attributes": {
        "name": "Alice",
        "email": "alice@example.com"
      }
    },
    {
      "id": 2,
      "type": "user",
      "attributes": {
        "name": "Bob",
        "email": "bob@example.com"
      }
    }
  ],
  "meta": {
    "pagination": {
      "current_page": 1,
      "per_page": 10,
      "total_pages": 5,
      "total_items": 50
    },
    "request_id": "xyz789-abc123-def456"
  }
}
```

#### Error Response Format
```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request contains invalid data",
    "details": [
      {
        "field": "email",
        "code": "INVALID_FORMAT",
        "message": "Email must be a valid email address"
      },
      {
        "field": "age",
        "code": "OUT_OF_RANGE",
        "message": "Age must be between 18 and 120"
      }
    ]
  },
  "meta": {
    "request_id": "error123-456789",
    "timestamp": "2023-01-15T10:30:00Z"
  }
}
```

### Content Negotiation
```http
# Client specifies preferred format
Accept: application/json
Accept: application/xml
Accept: application/json, application/xml;q=0.8

# Server responds with appropriate format
Content-Type: application/json
Content-Type: application/xml
```

## Authentication and Authorization {#auth}

### Authentication Methods

#### JWT (JSON Web Tokens)
```javascript
// JWT Structure: header.payload.signature
const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c";

// Usage in requests
const headers = {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json'
};
```

#### API Keys
```http
# Header-based
Authorization: ApiKey your-api-key-here
X-API-Key: your-api-key-here

# Query parameter
GET /api/v1/users?api_key=your-api-key-here
```

#### OAuth 2.0
```javascript
// Authorization Code Flow
const authUrl = 'https://auth.example.com/oauth/authorize?' +
  'client_id=your-client-id&' +
  'redirect_uri=https://yourapp.com/callback&' +
  'response_type=code&' +
  'scope=read write&' +
  'state=random-state-string';

// Token exchange
const tokenResponse = await fetch('https://auth.example.com/oauth/token', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded'
  },
  body: new URLSearchParams({
    grant_type: 'authorization_code',
    client_id: 'your-client-id',
    client_secret: 'your-client-secret',
    code: 'authorization-code-from-callback',
    redirect_uri: 'https://yourapp.com/callback'
  })
});
```

### Authorization Patterns

#### Role-Based Access Control (RBAC)
```json
{
  "user": {
    "id": 123,
    "roles": ["admin", "editor"],
    "permissions": [
      "users:read",
      "users:write",
      "products:read",
      "products:write"
    ]
  }
}
```

#### Attribute-Based Access Control (ABAC)
```json
{
  "subject": {
    "id": 123,
    "department": "sales",
    "level": "manager"
  },
  "resource": {
    "type": "customer_data",
    "owner": "sales_team",
    "classification": "confidential"
  },
  "action": "read",
  "environment": {
    "time": "business_hours",
    "location": "office"
  }
}
```

### Security Headers
```http
# Request headers
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
X-Request-ID: unique-request-identifier

# Response headers
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1609459200
```

## Error Handling {#error-handling}

### Comprehensive Error Responses

#### Validation Errors
```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "email",
        "value": "invalid-email",
        "code": "INVALID_EMAIL_FORMAT",
        "message": "Please provide a valid email address"
      },
      {
        "field": "password",
        "code": "PASSWORD_TOO_SHORT",
        "message": "Password must be at least 8 characters long"
      }
    ]
  },
  "meta": {
    "request_id": "req_123456789",
    "timestamp": "2023-01-15T10:30:00Z",
    "documentation_url": "https://docs.api.example.com/errors#validation"
  }
}
```

#### Business Logic Errors
```json
{
  "status": "error",
  "error": {
    "code": "INSUFFICIENT_FUNDS",
    "message": "Cannot process payment due to insufficient funds",
    "details": {
      "account_balance": 50.00,
      "required_amount": 75.00,
      "currency": "USD"
    }
  },
  "meta": {
    "request_id": "req_987654321",
    "timestamp": "2023-01-15T10:30:00Z"
  }
}
```

#### System Errors
```json
{
  "status": "error",
  "error": {
    "code": "SERVICE_UNAVAILABLE",
    "message": "The service is temporarily unavailable",
    "details": {
      "retry_after": 300,
      "estimated_resolution": "2023-01-15T11:00:00Z"
    }
  },
  "meta": {
    "request_id": "req_error_001",
    "timestamp": "2023-01-15T10:30:00Z"
  }
}
```

### Error Handling Implementation
```javascript
// Express.js error handling middleware
app.use((error, req, res, next) => {
  const errorResponse = {
    status: 'error',
    error: {
      code: error.code || 'INTERNAL_SERVER_ERROR',
      message: error.message || 'An unexpected error occurred'
    },
    meta: {
      request_id: req.id,
      timestamp: new Date().toISOString()
    }
  };

  // Add error details for validation errors
  if (error.type === 'validation') {
    errorResponse.error.details = error.details;
  }

  // Log error for monitoring
  logger.error('API Error', {
    error: error.stack,
    request_id: req.id,
    method: req.method,
    url: req.url,
    user_id: req.user?.id
  });

  res.status(error.statusCode || 500).json(errorResponse);
});
```

## Versioning Strategies {#versioning}

### URI Versioning
```http
GET /api/v1/users
GET /api/v2/users
GET /api/v3/users
```

### Header Versioning
```http
GET /api/users
Accept: application/vnd.api+json;version=1
Accept: application/vnd.api+json;version=2
```

### Query Parameter Versioning
```http
GET /api/users?version=1
GET /api/users?v=2
```

### Content Type Versioning
```http
GET /api/users
Accept: application/vnd.company.v1+json
Accept: application/vnd.company.v2+json
```

### Versioning Best Practices
```javascript
// Semantic versioning for APIs
const versions = {
  v1: {
    major: 1,
    minor: 0,
    patch: 0,
    deprecated: false,
    sunset_date: null
  },
  v2: {
    major: 2,
    minor: 1,
    patch: 3,
    deprecated: false,
    sunset_date: null
  },
  v1_deprecated: {
    major: 1,
    minor: 0,
    patch: 0,
    deprecated: true,
    sunset_date: '2024-12-31T23:59:59Z'
  }
};

// Deprecation headers
const deprecationHeaders = {
  'Deprecation': 'true',
  'Sunset': '2024-12-31T23:59:59Z',
  'Link': '<https://docs.api.example.com/migration>; rel="successor-version"'
};
```

## Caching and Performance {#performance}

### HTTP Caching Headers

#### Cache-Control
```http
# Public cache, 1 hour expiration
Cache-Control: public, max-age=3600

# Private cache, must revalidate
Cache-Control: private, must-revalidate

# No caching
Cache-Control: no-cache, no-store, must-revalidate
```

#### ETag and Conditional Requests
```http
# Initial request
GET /api/v1/users/123
Accept: application/json

# Response with ETag
HTTP/1.1 200 OK
ETag: "abc123def456"
Content-Type: application/json

# Conditional request
GET /api/v1/users/123
If-None-Match: "abc123def456"

# Not modified response
HTTP/1.1 304 Not Modified
ETag: "abc123def456"
```

#### Last-Modified and If-Modified-Since
```http
# Response with Last-Modified
HTTP/1.1 200 OK
Last-Modified: Wed, 15 Jan 2023 10:30:00 GMT
Content-Type: application/json

# Conditional request
GET /api/v1/users/123
If-Modified-Since: Wed, 15 Jan 2023 10:30:00 GMT

# Not modified response
HTTP/1.1 304 Not Modified
```

### Performance Optimization Techniques

#### Pagination
```javascript
// Offset-based pagination
const paginationParams = {
  page: 1,
  per_page: 20,
  offset: 0,
  limit: 20
};

// Cursor-based pagination (better for large datasets)
const cursorParams = {
  cursor: 'eyJpZCI6MTIzfQ==',
  limit: 20,
  direction: 'next'
};

// Response with pagination metadata
const paginatedResponse = {
  data: [...],
  meta: {
    pagination: {
      current_page: 1,
      per_page: 20,
      total_pages: 10,
      total_items: 200,
      has_next: true,
      has_previous: false,
      next_cursor: 'eyJpZCI6MTQzfQ==',
      previous_cursor: null
    }
  }
};
```

#### Field Selection and Inclusion
```http
# Select specific fields
GET /api/v1/users?fields=id,name,email

# Include related resources
GET /api/v1/users?include=profile,orders

# Exclude sensitive fields
GET /api/v1/users?exclude=internal_notes,private_data
```

#### Compression
```http
# Request compression support
Accept-Encoding: gzip, deflate, br

# Response with compression
Content-Encoding: gzip
Vary: Accept-Encoding
```

#### Rate Limiting
```javascript
// Rate limiting headers
const rateLimitHeaders = {
  'X-RateLimit-Limit': '1000',
  'X-RateLimit-Remaining': '999',
  'X-RateLimit-Reset': '1609459200',
  'X-RateLimit-Window': '3600'
};

// Rate limit exceeded response
const rateLimitResponse = {
  status: 'error',
  error: {
    code: 'RATE_LIMIT_EXCEEDED',
    message: 'API rate limit exceeded',
    details: {
      limit: 1000,
      window: 3600,
      reset_time: '2023-01-15T11:00:00Z'
    }
  }
};
```

## Security Best Practices {#security}

### Input Validation and Sanitization
```javascript
// Input validation schema
const userSchema = {
  name: {
    type: 'string',
    minLength: 2,
    maxLength: 100,
    pattern: '^[a-zA-Z\\s]+$'
  },
  email: {
    type: 'string',
    format: 'email',
    maxLength: 255
  },
  age: {
    type: 'integer',
    minimum: 18,
    maximum: 120
  }
};

// SQL injection prevention
const getUserById = async (id) => {
  // Use parameterized queries
  const query = 'SELECT * FROM users WHERE id = $1';
  const result = await db.query(query, [id]);
  return result.rows[0];
};
```

### HTTPS and Transport Security
```javascript
// Enforce HTTPS
app.use((req, res, next) => {
  if (!req.secure && req.get('x-forwarded-proto') !== 'https') {
    return res.redirect('https://' + req.get('host') + req.url);
  }
  next();
});

// Security headers
app.use((req, res, next) => {
  res.set({
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
    'Content-Security-Policy': "default-src 'self'"
  });
  next();
});
```

### CORS Configuration
```javascript
// CORS configuration
const corsOptions = {
  origin: ['https://app.example.com', 'https://admin.example.com'],
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Request-ID'],
  exposedHeaders: ['X-RateLimit-Limit', 'X-RateLimit-Remaining'],
  credentials: true,
  maxAge: 86400 // 24 hours
};

app.use(cors(corsOptions));
```

### API Security Checklist
```javascript
const securityChecklist = [
  '✓ Use HTTPS for all endpoints',
  '✓ Implement proper authentication',
  '✓ Validate and sanitize all inputs',
  '✓ Use parameterized queries',
  '✓ Implement rate limiting',
  '✓ Set security headers',
  '✓ Configure CORS properly',
  '✓ Log security events',
  '✓ Keep dependencies updated',
  '✓ Implement proper error handling',
  '✓ Use least privilege principle',
  '✓ Encrypt sensitive data'
];
```

## Documentation and Testing {#documentation}

### OpenAPI/Swagger Documentation
```yaml
# openapi.yaml
openapi: 3.0.3
info:
  title: User Management API
  description: A comprehensive API for managing users
  version: 1.0.0
  contact:
    name: API Support
    email: api-support@example.com
    url: https://example.com/support

servers:
  - url: https://api.example.com/v1
    description: Production server
  - url: https://staging-api.example.com/v1
    description: Staging server

paths:
  /users:
    get:
      summary: List users
      description: Retrieve a paginated list of users
      parameters:
        - name: page
          in: query
          description: Page number for pagination
          schema:
            type: integer
            minimum: 1
            default: 1
        - name: per_page
          in: query
          description: Number of items per page
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 10
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  meta:
                    $ref: '#/components/schemas/PaginationMeta'

components:
  schemas:
    User:
      type: object
      required:
        - id
        - name
        - email
      properties:
        id:
          type: integer
          example: 123
        name:
          type: string
          example: "John Doe"
        email:
          type: string
          format: email
          example: "john@example.com"
        created_at:
          type: string
          format: date-time
          example: "2023-01-15T10:30:00Z"
```

### API Testing
```javascript
// Unit tests for API endpoints
describe('User API', () => {
  describe('GET /api/v1/users', () => {
    it('should return list of users', async () => {
      const response = await request(app)
        .get('/api/v1/users')
        .set('Authorization', `Bearer ${validToken}`)
        .expect(200);

      expect(response.body).toHaveProperty('data');
      expect(response.body).toHaveProperty('meta');
      expect(Array.isArray(response.body.data)).toBe(true);
    });

    it('should support pagination', async () => {
      const response = await request(app)
        .get('/api/v1/users?page=2&per_page=5')
        .set('Authorization', `Bearer ${validToken}`)
        .expect(200);

      expect(response.body.meta.pagination.current_page).toBe(2);
      expect(response.body.meta.pagination.per_page).toBe(5);
    });
  });

  describe('POST /api/v1/users', () => {
    it('should create a new user', async () => {
      const userData = {
        name: 'Jane Doe',
        email: 'jane@example.com'
      };

      const response = await request(app)
        .post('/api/v1/users')
        .set('Authorization', `Bearer ${validToken}`)
        .send(userData)
        .expect(201);

      expect(response.body.data).toMatchObject(userData);
      expect(response.body.data).toHaveProperty('id');
    });

    it('should validate required fields', async () => {
      const invalidData = { name: 'Jane Doe' }; // Missing email

      const response = await request(app)
        .post('/api/v1/users')
        .set('Authorization', `Bearer ${validToken}`)
        .send(invalidData)
        .expect(422);

      expect(response.body.error.code).toBe('VALIDATION_ERROR');
    });
  });
});

// Integration tests
describe('User Management Flow', () => {
  it('should complete user lifecycle', async () => {
    // Create user
    const createResponse = await request(app)
      .post('/api/v1/users')
      .set('Authorization', `Bearer ${validToken}`)
      .send({ name: 'Test User', email: 'test@example.com' })
      .expect(201);

    const userId = createResponse.body.data.id;

    // Retrieve user
    await request(app)
      .get(`/api/v1/users/${userId}`)
      .set('Authorization', `Bearer ${validToken}`)
      .expect(200);

    // Update user
    await request(app)
      .put(`/api/v1/users/${userId}`)
      .set('Authorization', `Bearer ${validToken}`)
      .send({ name: 'Updated User', email: 'updated@example.com' })
      .expect(200);

    // Delete user
    await request(app)
      .delete(`/api/v1/users/${userId}`)
      .set('Authorization', `Bearer ${validToken}`)
      .expect(204);

    // Verify deletion
    await request(app)
      .get(`/api/v1/users/${userId}`)
      .set('Authorization', `Bearer ${validToken}`)
      .expect(404);
  });
});
```

This comprehensive guide covers the essential principles and practices for designing robust REST APIs. By following these guidelines, you'll create APIs that are intuitive, scalable, secure, and maintainable. Remember that REST is not just about using HTTP methods correctly, but about creating a well-designed, resource-oriented architecture that provides a great developer experience.

The key to successful API design is consistency, clear documentation, and continuous feedback from API consumers. Start with simple, clear endpoints and gradually add complexity as needed, always keeping the developer experience at the forefront of your design decisions.''',
            'category': 'Web Development',
            'tags': 'rest-api,web-services,http,api-design',
        },
        {
            'title': 'SQL Query Optimization',
            'content': '''# SQL Query Optimization: Mastering Database Performance

## Table of Contents
1. [Introduction to Query Optimization](#introduction)
2. [Understanding Query Execution](#execution)
3. [Indexing Strategies](#indexing)
4. [Query Analysis and Profiling](#analysis)
5. [Join Optimization](#joins)
6. [Subquery and CTE Optimization](#subqueries)
7. [Performance Tuning Techniques](#tuning)
8. [Database-Specific Optimizations](#database-specific)
9. [Monitoring and Maintenance](#monitoring)
10. [Best Practices and Anti-Patterns](#best-practices)

## Introduction to Query Optimization {#introduction}

SQL query optimization is the process of improving the performance of database queries by reducing execution time, resource consumption, and improving overall throughput. Efficient queries are crucial for application performance, especially as data volumes grow.

### Why Query Optimization Matters
- **Performance**: Faster query execution improves user experience
- **Scalability**: Optimized queries handle larger datasets efficiently
- **Resource Utilization**: Reduced CPU, memory, and I/O consumption
- **Cost Reduction**: Lower cloud infrastructure costs
- **Concurrency**: Better performance under high user loads

### Query Performance Factors
```sql
-- Factors affecting query performance:
-- 1. Table size and data distribution
-- 2. Index availability and quality
-- 3. Query complexity and structure
-- 4. Hardware resources (CPU, memory, storage)
-- 5. Database configuration
-- 6. Concurrent load

-- Example: Impact of proper indexing
-- Without index: O(n) linear scan
SELECT * FROM users WHERE email = 'john@example.com';

-- With index: O(log n) tree traversal
CREATE INDEX idx_users_email ON users(email);
```

### Query Optimization Process
```sql
-- 1. Identify slow queries
-- 2. Analyze execution plans
-- 3. Identify bottlenecks
-- 4. Apply optimization techniques
-- 5. Test and measure improvements
-- 6. Monitor ongoing performance
```

## Understanding Query Execution {#execution}

### Query Execution Phases
```sql
-- 1. Parsing: Syntax and semantic validation
-- 2. Optimization: Query plan generation
-- 3. Compilation: Plan compilation
-- 4. Execution: Data retrieval and processing

-- Example execution plan analysis
EXPLAIN (ANALYZE, BUFFERS) 
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at >= '2023-01-01'
GROUP BY u.id, u.name
ORDER BY order_count DESC
LIMIT 10;
```

### Reading Execution Plans
```sql
-- PostgreSQL execution plan example
/*
QUERY PLAN
Limit  (cost=1000.00..1000.25 rows=10 width=64)
  ->  Sort  (cost=1000.00..1000.50 rows=200 width=64)
        Sort Key: (count(o.id)) DESC
        ->  HashAggregate  (cost=800.00..950.00 rows=200 width=64)
              Group Key: u.id, u.name
              ->  Hash Left Join  (cost=400.00..750.00 rows=5000 width=32)
                    Hash Cond: (u.id = o.user_id)
                    ->  Seq Scan on users u  (cost=0.00..200.00 rows=1000 width=32)
                          Filter: (created_at >= '2023-01-01'::date)
                    ->  Hash  (cost=150.00..150.00 rows=10000 width=8)
                          ->  Seq Scan on orders o  (cost=0.00..150.00 rows=10000 width=8)
*/
```

### Cost-Based Optimization
```sql
-- Database optimizers use statistics to estimate costs
-- Update statistics regularly for accurate estimates
ANALYZE users;
ANALYZE orders;

-- View table statistics
SELECT 
    schemaname,
    tablename,
    n_tup_ins,
    n_tup_upd,
    n_tup_del,
    last_analyze,
    last_autoanalyze
FROM pg_stat_user_tables
WHERE tablename IN ('users', 'orders');
```

## Indexing Strategies {#indexing}

### Index Types and Use Cases

#### B-Tree Indexes (Default)
```sql
-- Best for equality and range queries
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_date ON orders(order_date);

-- Composite indexes for multiple columns
CREATE INDEX idx_orders_user_date ON orders(user_id, order_date);

-- Query examples that benefit from B-tree indexes
SELECT * FROM users WHERE email = 'john@example.com';
SELECT * FROM orders WHERE order_date BETWEEN '2023-01-01' AND '2023-12-31';
SELECT * FROM orders WHERE user_id = 123 AND order_date > '2023-06-01';
```

#### Hash Indexes
```sql
-- PostgreSQL hash indexes for equality queries
CREATE INDEX idx_users_status_hash ON users USING HASH(status);

-- Good for exact matches only
SELECT * FROM users WHERE status = 'active';
```

#### Partial Indexes
```sql
-- Index only rows that meet certain conditions
CREATE INDEX idx_active_users_email ON users(email) 
WHERE status = 'active';

CREATE INDEX idx_recent_orders ON orders(user_id) 
WHERE order_date >= '2023-01-01';

-- Significantly reduces index size and maintenance cost
```

#### Expression Indexes
```sql
-- Index on computed values
CREATE INDEX idx_users_lower_email ON users(LOWER(email));
CREATE INDEX idx_orders_total_amount ON orders((quantity * unit_price));

-- Enables efficient queries on expressions
SELECT * FROM users WHERE LOWER(email) = 'john@example.com';
SELECT * FROM orders WHERE (quantity * unit_price) > 1000;
```

#### Covering Indexes
```sql
-- Include additional columns for covering queries
CREATE INDEX idx_orders_covering ON orders(user_id, order_date) 
INCLUDE (total_amount, status);

-- Query can be satisfied entirely from index
SELECT total_amount, status 
FROM orders 
WHERE user_id = 123 AND order_date = '2023-06-15';
```

### Index Optimization Strategies
```sql
-- 1. Selectivity: Create indexes on highly selective columns
-- Good: email (unique values)
CREATE INDEX idx_users_email ON users(email);

-- Poor: gender (low selectivity)
-- CREATE INDEX idx_users_gender ON users(gender); -- Avoid

-- 2. Column order in composite indexes
-- Put most selective column first
CREATE INDEX idx_orders_user_status_date ON orders(user_id, status, order_date);

-- 3. Avoid over-indexing
-- Each index adds overhead for INSERT/UPDATE/DELETE operations
-- Monitor index usage
SELECT 
    indexrelname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;

-- Drop unused indexes
DROP INDEX IF EXISTS idx_unused_index;
```

## Query Analysis and Profiling {#analysis}

### Performance Monitoring Tools

#### PostgreSQL Query Analysis
```sql
-- Enable query logging
SET log_statement = 'all';
SET log_min_duration_statement = 1000; -- Log queries > 1 second

-- Use pg_stat_statements extension
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Find slowest queries
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    stddev_time,
    rows
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Reset statistics
SELECT pg_stat_statements_reset();
```

#### EXPLAIN ANALYZE
```sql
-- Detailed execution analysis
EXPLAIN (ANALYZE, BUFFERS, VERBOSE) 
SELECT 
    u.name,
    u.email,
    COUNT(o.id) as order_count,
    SUM(o.total_amount) as total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active'
  AND u.created_at >= '2023-01-01'
GROUP BY u.id, u.name, u.email
HAVING COUNT(o.id) > 5
ORDER BY total_spent DESC
LIMIT 20;

-- Key metrics to analyze:
-- - Actual Time vs Estimated Time
-- - Rows vs Estimated Rows  
-- - Buffer usage (shared hit, read, dirtied)
-- - Sort operations and memory usage
```

#### MySQL Query Profiling
```sql
-- Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;

-- Profile a specific query
SET profiling = 1;
SELECT * FROM users WHERE email = 'john@example.com';
SHOW PROFILES;
SHOW PROFILE FOR QUERY 1;

-- Performance Schema queries
SELECT 
    event_name,
    count_star,
    sum_timer_wait,
    avg_timer_wait
FROM performance_schema.events_statements_summary_by_digest
ORDER BY sum_timer_wait DESC
LIMIT 10;
```

### Query Pattern Analysis
```sql
-- Identify common anti-patterns

-- 1. N+1 Query Problem
-- Bad: Multiple queries in a loop
SELECT * FROM users WHERE status = 'active';
-- For each user: SELECT * FROM orders WHERE user_id = ?

-- Good: Single query with JOIN
SELECT 
    u.*,
    o.id as order_id,
    o.total_amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active';

-- 2. SELECT * antipattern
-- Bad: Retrieving unnecessary columns
SELECT * FROM users WHERE id = 123;

-- Good: Select only needed columns
SELECT id, name, email FROM users WHERE id = 123;

-- 3. Missing WHERE clauses
-- Bad: Full table scan
SELECT COUNT(*) FROM orders;

-- Good: Use appropriate filters
SELECT COUNT(*) FROM orders WHERE order_date >= '2023-01-01';
```

## Join Optimization {#joins}

### Join Types and Performance

#### Inner Joins
```sql
-- Most efficient when both tables have appropriate indexes
SELECT 
    u.name,
    o.order_date,
    o.total_amount
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active'
  AND o.order_date >= '2023-01-01';

-- Ensure indexes exist on join columns
CREATE INDEX idx_users_id ON users(id);
CREATE INDEX idx_orders_user_id ON orders(user_id);
```

#### Left/Right Outer Joins
```sql
-- Be careful with large result sets
SELECT 
    u.name,
    COALESCE(COUNT(o.id), 0) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at >= '2023-01-01'
GROUP BY u.id, u.name;

-- Consider using EXISTS for existence checks
SELECT u.name
FROM users u
WHERE EXISTS (
    SELECT 1 FROM orders o 
    WHERE o.user_id = u.id 
    AND o.order_date >= '2023-01-01'
);
```

#### Join Algorithms
```sql
-- 1. Nested Loop Join
-- Good for small datasets, indexed joins
-- Avoid for large tables without indexes

-- 2. Hash Join
-- Good for large datasets, equality joins
-- Requires sufficient memory

-- 3. Sort Merge Join
-- Good for large datasets, range joins
-- Benefits from sorted data

-- Force specific join algorithm (PostgreSQL)
SET enable_nestloop = OFF;
SET enable_hashjoin = ON;
SET enable_mergejoin = ON;
```

### Join Optimization Techniques
```sql
-- 1. Join order optimization
-- Filter early, join late
SELECT 
    u.name,
    recent_orders.total_spent
FROM users u
INNER JOIN (
    SELECT 
        user_id,
        SUM(total_amount) as total_spent
    FROM orders
    WHERE order_date >= '2023-11-01'  -- Filter early
    GROUP BY user_id
) recent_orders ON u.id = recent_orders.user_id
WHERE u.status = 'active';

-- 2. Avoid Cartesian products
-- Always specify join conditions
-- Bad
SELECT * FROM users u, orders o WHERE u.status = 'active';

-- Good
SELECT * FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active';

-- 3. Use appropriate join types
-- EXISTS vs IN vs JOIN
-- EXISTS is often more efficient for existence checks
SELECT u.name
FROM users u
WHERE EXISTS (
    SELECT 1 FROM orders o
    WHERE o.user_id = u.id AND o.status = 'completed'
);
```

## Subquery and CTE Optimization {#subqueries}

### Subquery Types and Performance

#### Correlated vs Non-Correlated Subqueries
```sql
-- Non-correlated subquery (generally faster)
SELECT name
FROM users
WHERE id IN (
    SELECT user_id 
    FROM orders 
    WHERE order_date >= '2023-01-01'
);

-- Correlated subquery (executed for each row)
SELECT name
FROM users u
WHERE EXISTS (
    SELECT 1 
    FROM orders o
    WHERE o.user_id = u.id 
    AND o.order_date >= '2023-01-01'
);

-- Often better to rewrite as JOIN
SELECT DISTINCT u.name
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.order_date >= '2023-01-01';
```

#### Scalar Subqueries
```sql
-- Scalar subquery in SELECT (can be expensive)
SELECT 
    u.name,
    u.email,
    (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) as order_count
FROM users u;

-- Better: Use LEFT JOIN with aggregation
SELECT 
    u.name,
    u.email,
    COALESCE(o.order_count, 0) as order_count
FROM users u
LEFT JOIN (
    SELECT user_id, COUNT(*) as order_count
    FROM orders
    GROUP BY user_id
) o ON u.id = o.user_id;
```

### Common Table Expressions (CTEs)
```sql
-- Simple CTE
WITH active_users AS (
    SELECT id, name, email
    FROM users
    WHERE status = 'active' AND created_at >= '2023-01-01'
),
user_orders AS (
    SELECT 
        u.id,
        u.name,
        COUNT(o.id) as order_count,
        SUM(o.total_amount) as total_spent
    FROM active_users u
    LEFT JOIN orders o ON u.id = o.user_id
    GROUP BY u.id, u.name
)
SELECT *
FROM user_orders
WHERE order_count > 5
ORDER BY total_spent DESC;

-- Recursive CTE for hierarchical data
WITH RECURSIVE category_hierarchy AS (
    -- Base case
    SELECT id, name, parent_id, 1 as level
    FROM categories
    WHERE parent_id IS NULL
    
    UNION ALL
    
    -- Recursive case
    SELECT c.id, c.name, c.parent_id, ch.level + 1
    FROM categories c
    INNER JOIN category_hierarchy ch ON c.parent_id = ch.id
)
SELECT * FROM category_hierarchy ORDER BY level, name;
```

### Window Functions vs Subqueries
```sql
-- Using subquery (less efficient)
SELECT 
    user_id,
    order_date,
    total_amount,
    (SELECT AVG(total_amount) 
     FROM orders o2 
     WHERE o2.user_id = o1.user_id) as user_avg
FROM orders o1;

-- Using window function (more efficient)
SELECT 
    user_id,
    order_date,
    total_amount,
    AVG(total_amount) OVER (PARTITION BY user_id) as user_avg
FROM orders;

-- Ranking with window functions
SELECT 
    user_id,
    order_date,
    total_amount,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY order_date DESC) as order_rank
FROM orders;
```

## Performance Tuning Techniques {#tuning}

### Query Rewriting Techniques

#### Predicate Pushdown
```sql
-- Bad: Filter after join
SELECT u.name, o.total_amount
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.order_date >= '2023-01-01';

-- Good: Filter before join
SELECT u.name, recent_orders.total_amount
FROM users u
INNER JOIN (
    SELECT user_id, total_amount
    FROM orders
    WHERE order_date >= '2023-01-01'  -- Filter pushed down
) recent_orders ON u.id = recent_orders.user_id;
```

#### Projection Pushdown
```sql
-- Bad: Select all columns then filter
SELECT name, email
FROM (
    SELECT * FROM users WHERE status = 'active'
) active_users;

-- Good: Select only needed columns
SELECT name, email
FROM users
WHERE status = 'active';
```

#### Aggregate Pushdown
```sql
-- Bad: Aggregate after join
SELECT 
    u.name,
    SUM(o.total_amount) as total_spent
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active'
GROUP BY u.id, u.name;

-- Good: Pre-aggregate before join
SELECT 
    u.name,
    user_totals.total_spent
FROM users u
INNER JOIN (
    SELECT user_id, SUM(total_amount) as total_spent
    FROM orders
    GROUP BY user_id
) user_totals ON u.id = user_totals.user_id
WHERE u.status = 'active';
```

### Partitioning Strategies
```sql
-- Range partitioning by date
CREATE TABLE orders_2023 PARTITION OF orders
FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');

CREATE TABLE orders_2024 PARTITION OF orders
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

-- Hash partitioning by user_id
CREATE TABLE orders_p0 PARTITION OF orders
FOR VALUES WITH (MODULUS 4, REMAINDER 0);

CREATE TABLE orders_p1 PARTITION OF orders
FOR VALUES WITH (MODULUS 4, REMAINDER 1);

-- Partition pruning in action
SELECT * FROM orders 
WHERE order_date >= '2023-06-01' 
  AND order_date < '2023-07-01';
-- Only scans orders_2023 partition
```

### Materialized Views
```sql
-- Create materialized view for expensive aggregations
CREATE MATERIALIZED VIEW user_order_summary AS
SELECT 
    u.id,
    u.name,
    u.email,
    COUNT(o.id) as order_count,
    SUM(o.total_amount) as total_spent,
    MAX(o.order_date) as last_order_date
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name, u.email;

-- Create index on materialized view
CREATE INDEX idx_user_order_summary_total_spent 
ON user_order_summary(total_spent DESC);

-- Refresh materialized view
REFRESH MATERIALIZED VIEW user_order_summary;

-- Use in queries
SELECT * FROM user_order_summary
WHERE total_spent > 1000
ORDER BY total_spent DESC;
```

## Database-Specific Optimizations {#database-specific}

### PostgreSQL Optimizations
```sql
-- Configuration tuning
-- postgresql.conf
shared_buffers = '256MB'          -- 25% of RAM
effective_cache_size = '1GB'      -- Available OS cache
work_mem = '4MB'                  -- Per operation memory
maintenance_work_mem = '64MB'     -- For maintenance operations
random_page_cost = 1.1            -- SSD optimization

-- VACUUM and ANALYZE
VACUUM ANALYZE users;             -- Reclaim space and update stats
REINDEX INDEX idx_users_email;    -- Rebuild fragmented index

-- Parallel query execution
SET max_parallel_workers_per_gather = 2;
EXPLAIN (ANALYZE, BUFFERS)
SELECT COUNT(*) FROM large_table WHERE condition = 'value';
```

### MySQL Optimizations
```sql
-- Configuration tuning
-- my.cnf
innodb_buffer_pool_size = 1G      -- 70-80% of RAM
innodb_log_file_size = 256M       -- Large redo logs
query_cache_size = 128M           -- Query result cache
tmp_table_size = 128M             -- Temporary table size

-- Index hints
SELECT /*+ USE_INDEX(users, idx_users_email) */ 
    name, email 
FROM users 
WHERE email = 'john@example.com';

-- Optimizer hints
SELECT /*+ JOIN_ORDER(u, o) */ 
    u.name, o.total_amount
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- Partitioning
CREATE TABLE orders (
    id INT AUTO_INCREMENT,
    user_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2),
    PRIMARY KEY (id, order_date)
)
PARTITION BY RANGE (YEAR(order_date)) (
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION pmax VALUES LESS THAN MAXVALUE
);
```

### SQL Server Optimizations
```sql
-- Index recommendations
SELECT 
    migs.avg_total_user_cost * (migs.avg_user_impact / 100.0) * (migs.user_seeks + migs.user_scans) AS improvement_measure,
    'CREATE INDEX [missing_index_' + CONVERT(varchar, mig.index_group_handle) + '_' + CONVERT(varchar, mid.index_handle) + ']'
    + ' ON ' + mid.statement + ' (' + ISNULL(mid.equality_columns,'') 
    + CASE WHEN mid.equality_columns IS NOT NULL AND mid.inequality_columns IS NOT NULL THEN ',' ELSE '' END
    + ISNULL(mid.inequality_columns, '') + ')' 
    + ISNULL(' INCLUDE (' + mid.included_columns + ')', '') AS create_index_statement
FROM sys.dm_db_missing_index_groups mig
INNER JOIN sys.dm_db_missing_index_group_stats migs ON migs.group_handle = mig.index_group_handle
INNER JOIN sys.dm_db_missing_index_details mid ON mig.index_handle = mid.index_handle
ORDER BY improvement_measure DESC;

-- Query Store
ALTER DATABASE MyDatabase SET QUERY_STORE = ON;

-- Columnstore indexes for analytics
CREATE CLUSTERED COLUMNSTORE INDEX cci_orders_analytics
ON orders_analytics;

-- In-memory OLTP
CREATE TABLE users_memory (
    id INT IDENTITY PRIMARY KEY NONCLUSTERED,
    name NVARCHAR(100),
    email NVARCHAR(255),
    INDEX ix_email HASH (email) WITH (BUCKET_COUNT = 1000000)
) WITH (MEMORY_OPTIMIZED = ON, DURABILITY = SCHEMA_AND_DATA);
```

## Monitoring and Maintenance {#monitoring}

### Performance Monitoring Queries
```sql
-- PostgreSQL monitoring
-- Active queries
SELECT 
    pid,
    now() - pg_stat_activity.query_start AS duration,
    query,
    state
FROM pg_stat_activity
WHERE (now() - pg_stat_activity.query_start) > interval '5 minutes';

-- Lock monitoring
SELECT 
    blocked_locks.pid AS blocked_pid,
    blocked_activity.usename AS blocked_user,
    blocking_locks.pid AS blocking_pid,
    blocking_activity.usename AS blocking_user,
    blocked_activity.query AS blocked_statement
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;

-- Index usage statistics
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

### Automated Monitoring Setup
```sql
-- Create monitoring views
CREATE VIEW slow_queries AS
SELECT 
    query,
    calls,
    total_time / 1000.0 AS total_seconds,
    mean_time / 1000.0 AS mean_seconds,
    stddev_time / 1000.0 AS stddev_seconds,
    rows,
    100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
FROM pg_stat_statements
WHERE mean_time > 1000  -- Queries taking more than 1 second on average
ORDER BY mean_time DESC;

-- Maintenance procedures
CREATE OR REPLACE FUNCTION maintenance_routine()
RETURNS void AS $$
BEGIN
    -- Update table statistics
    ANALYZE;
    
    -- Vacuum tables with high update/delete activity
    VACUUM (ANALYZE, VERBOSE) users;
    VACUUM (ANALYZE, VERBOSE) orders;
    
    -- Reindex if fragmentation is high
    REINDEX INDEX CONCURRENTLY idx_users_email;
    
    -- Log completion
    INSERT INTO maintenance_log (run_date, action, status)
    VALUES (NOW(), 'routine_maintenance', 'completed');
END;
$$ LANGUAGE plpgsql;

-- Schedule maintenance
SELECT cron.schedule('maintenance', '0 2 * * 0', 'SELECT maintenance_routine();');
```

## Best Practices and Anti-Patterns {#best-practices}

### Query Optimization Best Practices
```sql
-- 1. Always use appropriate WHERE clauses
-- Good
SELECT * FROM orders WHERE user_id = 123 AND order_date >= '2023-01-01';

-- Bad
SELECT * FROM orders; -- Full table scan

-- 2. Use LIMIT for large result sets
-- Good
SELECT * FROM users ORDER BY created_at DESC LIMIT 100;

-- Bad
SELECT * FROM users ORDER BY created_at DESC; -- Returns all rows

-- 3. Avoid functions in WHERE clauses on indexed columns
-- Bad
SELECT * FROM users WHERE YEAR(created_at) = 2023;

-- Good
SELECT * FROM users WHERE created_at >= '2023-01-01' AND created_at < '2024-01-01';

-- 4. Use appropriate data types
-- Good
CREATE TABLE events (
    id BIGINT PRIMARY KEY,
    event_date DATE,            -- Not TIMESTAMP if time not needed
    status SMALLINT,            -- Not INT for small values
    amount DECIMAL(10,2)        -- Not FLOAT for money
);

-- 5. Normalize appropriately (avoid over-normalization)
-- Good balance between normalization and performance
```

### Common Anti-Patterns to Avoid
```sql
-- 1. SELECT * antipattern
-- Bad
SELECT * FROM users u
JOIN orders o ON u.id = o.user_id;

-- Good
SELECT u.name, u.email, o.total_amount, o.order_date
FROM users u
JOIN orders o ON u.id = o.user_id;

-- 2. N+1 query problem
-- Bad (in application code)
users = SELECT * FROM users WHERE status = 'active';
for user in users:
    orders = SELECT * FROM orders WHERE user_id = user.id;

-- Good
SELECT u.*, o.id as order_id, o.total_amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active';

-- 3. Inefficient pagination
-- Bad
SELECT * FROM products ORDER BY name LIMIT 1000 OFFSET 50000;

-- Good (cursor-based pagination)
SELECT * FROM products 
WHERE name > 'last_seen_name'
ORDER BY name 
LIMIT 1000;

-- 4. Correlated subqueries when joins would be better
-- Bad
SELECT u.name,
    (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) as order_count
FROM users u;

-- Good
SELECT u.name, COALESCE(o.order_count, 0) as order_count
FROM users u
LEFT JOIN (
    SELECT user_id, COUNT(*) as order_count
    FROM orders
    GROUP BY user_id
) o ON u.id = o.user_id;
```

### Performance Testing and Benchmarking
```sql
-- Create test data for benchmarking
INSERT INTO users (name, email, status, created_at)
SELECT 
    'User ' || generate_series,
    'user' || generate_series || '@example.com',
    CASE WHEN random() > 0.1 THEN 'active' ELSE 'inactive' END,
    NOW() - (random() * interval '2 years')
FROM generate_series(1, 1000000);

-- Benchmark queries with timing
\timing on

-- Test different query approaches
EXPLAIN (ANALYZE, BUFFERS) 
SELECT COUNT(*) FROM users WHERE status = 'active';

EXPLAIN (ANALYZE, BUFFERS)
SELECT COUNT(*) FROM users WHERE status = 'active' AND created_at >= '2023-01-01';

-- Compare index strategies
CREATE INDEX idx_users_status ON users(status);
CREATE INDEX idx_users_status_date ON users(status, created_at);

-- Measure improvement
\timing off
```

This comprehensive guide provides the foundation for optimizing SQL queries effectively. Remember that optimization is an iterative process - measure performance before and after changes, focus on the queries that matter most to your application, and maintain a balance between query performance and maintainability.

The key to successful query optimization is understanding your data, monitoring query performance continuously, and applying the right techniques for your specific use case. Start with the basics (proper indexing and WHERE clauses) and gradually move to more advanced techniques as needed.''',
            'category': 'Programming',
            'tags': 'sql,database,optimization,performance',
        },
        
        # New comprehensive articles for all categories
        {
            'title': 'Data Structures Mastery',
            'content': '''# Data Structures Mastery: Complete Algorithm Foundation

## Table of Contents
1. [Introduction to Data Structures](#introduction)
2. [Arrays and Dynamic Arrays](#arrays)
3. [Linked Lists](#linked-lists)
4. [Stacks and Queues](#stacks-queues)
5. [Trees and Binary Search Trees](#trees)
6. [Hash Tables and Hash Maps](#hash-tables)
7. [Heaps and Priority Queues](#heaps)
8. [Graphs and Graph Algorithms](#graphs)
9. [Advanced Data Structures](#advanced)
10. [Time and Space Complexity Analysis](#complexity)

## Introduction to Data Structures {#introduction}

Data structures are fundamental building blocks of computer science that organize and store data efficiently. Understanding data structures is crucial for writing efficient algorithms and solving complex programming problems.

### Why Data Structures Matter
- **Efficiency**: Choose the right structure for optimal performance
- **Memory Management**: Efficient use of system resources
- **Problem Solving**: Foundation for algorithmic thinking
- **Scalability**: Handle growing amounts of data
- **Code Organization**: Better software architecture

### Big O Notation Primer
```python
# O(1) - Constant Time
def get_first_element(arr):
    return arr[0] if arr else None

# O(n) - Linear Time
def find_element(arr, target):
    for element in arr:
        if element == target:
            return True
    return False

# O(n²) - Quadratic Time
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

# O(log n) - Logarithmic Time
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

## Arrays and Dynamic Arrays {#arrays}

### Static Arrays
```python
class StaticArray:
    def __init__(self, capacity):
        self.capacity = capacity
        self.data = [None] * capacity
        self.size = 0
    
    def get(self, index):
        if 0 <= index < self.size:
            return self.data[index]
        raise IndexError("Index out of bounds")
    
    def set(self, index, value):
        if 0 <= index < self.size:
            self.data[index] = value
        else:
            raise IndexError("Index out of bounds")
    
    def append(self, value):
        if self.size < self.capacity:
            self.data[self.size] = value
            self.size += 1
        else:
            raise OverflowError("Array is full")
    
    def __len__(self):
        return self.size
    
    def __str__(self):
        return str(self.data[:self.size])

# Usage
arr = StaticArray(5)
arr.append(1)
arr.append(2)
arr.append(3)
print(arr)  # [1, 2, 3]
```

### Dynamic Arrays (Resizable)
```python
class DynamicArray:
    def __init__(self):
        self.capacity = 2
        self.size = 0
        self.data = [None] * self.capacity
    
    def _resize(self, new_capacity):
        """Resize the underlying array."""
        old_data = self.data
        self.data = [None] * new_capacity
        self.capacity = new_capacity
        
        for i in range(self.size):
            self.data[i] = old_data[i]
    
    def append(self, value):
        """Add element to the end - O(1) amortized."""
        if self.size >= self.capacity:
            self._resize(2 * self.capacity)
        
        self.data[self.size] = value
        self.size += 1
    
    def get(self, index):
        """Get element at index - O(1)."""
        if 0 <= index < self.size:
            return self.data[index]
        raise IndexError("Index out of bounds")
    
    def set(self, index, value):
        """Set element at index - O(1)."""
        if 0 <= index < self.size:
            self.data[index] = value
        else:
            raise IndexError("Index out of bounds")
    
    def insert(self, index, value):
        """Insert element at index - O(n)."""
        if index < 0 or index > self.size:
            raise IndexError("Index out of bounds")
        
        if self.size >= self.capacity:
            self._resize(2 * self.capacity)
        
        # Shift elements to the right
        for i in range(self.size, index, -1):
            self.data[i] = self.data[i - 1]
        
        self.data[index] = value
        self.size += 1
    
    def delete(self, index):
        """Delete element at index - O(n)."""
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")
        
        # Shift elements to the left
        for i in range(index, self.size - 1):
            self.data[i] = self.data[i + 1]
        
        self.size -= 1
        
        # Shrink if necessary
        if self.size <= self.capacity // 4 and self.capacity > 2:
            self._resize(self.capacity // 2)
    
    def find(self, value):
        """Find first occurrence of value - O(n)."""
        for i in range(self.size):
            if self.data[i] == value:
                return i
        return -1
    
    def __len__(self):
        return self.size
    
    def __str__(self):
        return str([self.data[i] for i in range(self.size)])

# Advanced array operations
class ArrayOperations:
    @staticmethod
    def merge_sorted_arrays(arr1, arr2):
        """Merge two sorted arrays - O(n + m)."""
        result = []
        i = j = 0
        
        while i < len(arr1) and j < len(arr2):
            if arr1[i] <= arr2[j]:
                result.append(arr1[i])
                i += 1
            else:
                result.append(arr2[j])
                j += 1
        
        # Add remaining elements
        result.extend(arr1[i:])
        result.extend(arr2[j:])
        
        return result
    
    @staticmethod
    def rotate_array(arr, k):
        """Rotate array to the right by k positions - O(n)."""
        if not arr or k == 0:
            return arr
        
        n = len(arr)
        k = k % n  # Handle k > n
        
        def reverse(start, end):
            while start < end:
                arr[start], arr[end] = arr[end], arr[start]
                start += 1
                end -= 1
        
        # Reverse entire array
        reverse(0, n - 1)
        # Reverse first k elements
        reverse(0, k - 1)
        # Reverse remaining elements
        reverse(k, n - 1)
        
        return arr
    
    @staticmethod
    def find_max_subarray_sum(arr):
        """Kadane's algorithm for maximum subarray sum - O(n)."""
        if not arr:
            return 0
        
        max_sum = current_sum = arr[0]
        
        for i in range(1, len(arr)):
            current_sum = max(arr[i], current_sum + arr[i])
            max_sum = max(max_sum, current_sum)
        
        return max_sum
```

## Linked Lists {#linked-lists}

### Singly Linked List
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    
    def __str__(self):
        return str(self.val)

class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0
    
    def append(self, val):
        """Add element to the end - O(n)."""
        new_node = ListNode(val)
        
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        
        self.size += 1
    
    def prepend(self, val):
        """Add element to the beginning - O(1)."""
        new_node = ListNode(val)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
    
    def insert(self, index, val):
        """Insert element at index - O(n)."""
        if index < 0 or index > self.size:
            raise IndexError("Index out of bounds")
        
        if index == 0:
            self.prepend(val)
            return
        
        new_node = ListNode(val)
        current = self.head
        
        for _ in range(index - 1):
            current = current.next
        
        new_node.next = current.next
        current.next = new_node
        self.size += 1
    
    def delete(self, val):
        """Delete first occurrence of value - O(n)."""
        if not self.head:
            return False
        
        if self.head.val == val:
            self.head = self.head.next
            self.size -= 1
            return True
        
        current = self.head
        while current.next:
            if current.next.val == val:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        
        return False
    
    def find(self, val):
        """Find element - O(n)."""
        current = self.head
        index = 0
        
        while current:
            if current.val == val:
                return index
            current = current.next
            index += 1
        
        return -1
    
    def reverse(self):
        """Reverse the linked list - O(n)."""
        prev = None
        current = self.head
        
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        
        self.head = prev
    
    def get_middle(self):
        """Find middle element using two pointers - O(n)."""
        if not self.head:
            return None
        
        slow = fast = self.head
        
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        
        return slow.val
    
    def has_cycle(self):
        """Detect cycle using Floyd's algorithm - O(n)."""
        if not self.head:
            return False
        
        slow = fast = self.head
        
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            
            if slow == fast:
                return True
        
        return False
    
    def __len__(self):
        return self.size
    
    def __str__(self):
        if not self.head:
            return "[]"
        
        result = []
        current = self.head
        while current:
            result.append(str(current.val))
            current = current.next
        
        return " -> ".join(result)
```

### Doubly Linked List
```python
class DoublyListNode:
    def __init__(self, val=0, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next

class DoublyLinkedList:
    def __init__(self):
        # Dummy head and tail nodes
        self.head = DoublyListNode()
        self.tail = DoublyListNode()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0
    
    def append(self, val):
        """Add element to the end - O(1)."""
        new_node = DoublyListNode(val)
        prev_node = self.tail.prev
        
        prev_node.next = new_node
        new_node.prev = prev_node
        new_node.next = self.tail
        self.tail.prev = new_node
        
        self.size += 1
    
    def prepend(self, val):
        """Add element to the beginning - O(1)."""
        new_node = DoublyListNode(val)
        next_node = self.head.next
        
        self.head.next = new_node
        new_node.prev = self.head
        new_node.next = next_node
        next_node.prev = new_node
        
        self.size += 1
    
    def delete_node(self, node):
        """Delete a specific node - O(1)."""
        if node == self.head or node == self.tail:
            return False
        
        prev_node = node.prev
        next_node = node.next
        
        prev_node.next = next_node
        next_node.prev = prev_node
        
        self.size -= 1
        return True
    
    def find_node(self, val):
        """Find node with value - O(n)."""
        current = self.head.next
        
        while current != self.tail:
            if current.val == val:
                return current
            current = current.next
        
        return None
    
    def __str__(self):
        if self.size == 0:
            return "[]"
        
        result = []
        current = self.head.next
        
        while current != self.tail:
            result.append(str(current.val))
            current = current.next
        
        return " <-> ".join(result)
```

## Stacks and Queues {#stacks-queues}

### Stack Implementation
```python
class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, item):
        """Add item to top - O(1)."""
        self.items.append(item)
    
    def pop(self):
        """Remove and return top item - O(1)."""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items.pop()
    
    def peek(self):
        """Return top item without removing - O(1)."""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items[-1]
    
    def is_empty(self):
        """Check if stack is empty - O(1)."""
        return len(self.items) == 0
    
    def size(self):
        """Return number of items - O(1)."""
        return len(self.items)
    
    def __str__(self):
        return str(self.items)

# Stack Applications
class StackApplications:
    @staticmethod
    def is_balanced_parentheses(s):
        """Check if parentheses are balanced - O(n)."""
        stack = Stack()
        pairs = {'(': ')', '[': ']', '{': '}'}
        
        for char in s:
            if char in pairs:  # Opening bracket
                stack.push(char)
            elif char in pairs.values():  # Closing bracket
                if stack.is_empty():
                    return False
                
                opening = stack.pop()
                if pairs[opening] != char:
                    return False
        
        return stack.is_empty()
    
    @staticmethod
    def evaluate_postfix(expression):
        """Evaluate postfix expression - O(n)."""
        stack = Stack()
        operators = {'+', '-', '*', '/'}
        
        for token in expression.split():
            if token in operators:
                if stack.size() < 2:
                    raise ValueError("Invalid expression")
                
                b = stack.pop()
                a = stack.pop()
                
                if token == '+':
                    result = a + b
                elif token == '-':
                    result = a - b
                elif token == '*':
                    result = a * b
                elif token == '/':
                    result = a / b
                
                stack.push(result)
            else:
                stack.push(float(token))
        
        if stack.size() != 1:
            raise ValueError("Invalid expression")
        
        return stack.pop()
    
    @staticmethod
    def infix_to_postfix(expression):
        """Convert infix to postfix notation - O(n)."""
        stack = Stack()
        result = []
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
        
        for char in expression:
            if char.isalnum():  # Operand
                result.append(char)
            elif char == '(':
                stack.push(char)
            elif char == ')':
                while not stack.is_empty() and stack.peek() != '(':
                    result.append(stack.pop())
                stack.pop()  # Remove '('
            elif char in precedence:
                while (not stack.is_empty() and 
                       stack.peek() != '(' and
                       precedence.get(stack.peek(), 0) >= precedence[char]):
                    result.append(stack.pop())
                stack.push(char)
        
        while not stack.is_empty():
            result.append(stack.pop())
        
        return ''.join(result)
```

### Queue Implementation
```python
from collections import deque

class Queue:
    def __init__(self):
        self.items = deque()
    
    def enqueue(self, item):
        """Add item to rear - O(1)."""
        self.items.append(item)
    
    def dequeue(self):
        """Remove and return front item - O(1)."""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.items.popleft()
    
    def front(self):
        """Return front item without removing - O(1)."""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.items[0]
    
    def is_empty(self):
        """Check if queue is empty - O(1)."""
        return len(self.items) == 0
    
    def size(self):
        """Return number of items - O(1)."""
        return len(self.items)
    
    def __str__(self):
        return str(list(self.items))

class CircularQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.front = 0
        self.rear = -1
        self.size = 0
    
    def enqueue(self, item):
        """Add item to rear - O(1)."""
        if self.is_full():
            raise OverflowError("Queue is full")
        
        self.rear = (self.rear + 1) % self.capacity
        self.queue[self.rear] = item
        self.size += 1
    
    def dequeue(self):
        """Remove and return front item - O(1)."""
        if self.is_empty():
            raise IndexError("Queue is empty")
        
        item = self.queue[self.front]
        self.queue[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        
        return item
    
    def is_empty(self):
        return self.size == 0
    
    def is_full(self):
        return self.size == self.capacity
    
    def __str__(self):
        if self.is_empty():
            return "[]"
        
        result = []
        for i in range(self.size):
            index = (self.front + i) % self.capacity
            result.append(str(self.queue[index]))
        
        return "[" + ", ".join(result) + "]"

# Priority Queue (Min-Heap based)
import heapq

class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.index = 0
    
    def enqueue(self, item, priority):
        """Add item with priority - O(log n)."""
        heapq.heappush(self.heap, (priority, self.index, item))
        self.index += 1
    
    def dequeue(self):
        """Remove and return highest priority item - O(log n)."""
        if self.is_empty():
            raise IndexError("Priority queue is empty")
        
        priority, _, item = heapq.heappop(self.heap)
        return item
    
    def peek(self):
        """Return highest priority item without removing - O(1)."""
        if self.is_empty():
            raise IndexError("Priority queue is empty")
        
        return self.heap[0][2]
    
    def is_empty(self):
        return len(self.heap) == 0
    
    def size(self):
        return len(self.heap)
```

This comprehensive guide covers the fundamental data structures that every programmer should master. Understanding these structures and their operations is crucial for solving algorithmic problems efficiently and building scalable software systems.

Each data structure has its strengths and optimal use cases. The key is understanding when to use which structure based on the specific requirements of your problem, such as the types of operations you need to perform and their frequency.''',
            'category': 'Data Structure & Algorithms',
            'tags': 'algorithms,data-structures,complexity,optimization',
        },
        {
            'title': 'Python Deep Dive',
            'content': '''# Python Deep Dive: Advanced Programming Mastery

## Table of Contents
1. [Advanced Python Features](#advanced-features)
2. [Object-Oriented Programming](#oop)
3. [Metaclasses and Descriptors](#metaclasses)
4. [Decorators and Context Managers](#decorators)
5. [Concurrency and Parallelism](#concurrency)
6. [Memory Management](#memory)
7. [Performance Optimization](#performance)
8. [Design Patterns in Python](#patterns)
9. [Testing and Debugging](#testing)
10. [Python Internals](#internals)

## Advanced Python Features {#advanced-features}

### Generators and Iterators
```python
# Custom Iterator
class NumberSquares:
    def __init__(self, max_num):
        self.max_num = max_num
        self.current = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current >= self.max_num:
            raise StopIteration
        else:
            result = self.current ** 2
            self.current += 1
            return result

# Generator Function
def fibonacci_generator(n):
    """Generate Fibonacci sequence up to n terms."""
    a, b = 0, 1
    count = 0
    while count < n:
        yield a
        a, b = b, a + b
        count += 1

# Generator Expression
squares = (x**2 for x in range(10))

# Advanced Generator with send()
def accumulator():
    """Generator that accumulates sent values."""
    total = 0
    while True:
        value = yield total
        if value is not None:
            total += value

# Usage
acc = accumulator()
next(acc)  # Initialize
print(acc.send(10))  # 10
print(acc.send(5))   # 15
print(acc.send(3))   # 18

# Generator for large datasets
def read_large_file(file_path):
    """Memory-efficient file reader."""
    with open(file_path, 'r') as file:
        for line in file:
            yield line.strip()

# Coroutine example
def grep_coroutine(pattern):
    """Coroutine that searches for pattern in sent lines."""
    print(f"Searching for '{pattern}'")
    try:
        while True:
            line = yield
            if pattern in line:
                print(f"Found: {line}")
    except GeneratorExit:
        print("Coroutine closing")

# Usage
searcher = grep_coroutine("error")
next(searcher)  # Prime the coroutine
searcher.send("This is an error message")
searcher.send("Normal log entry")
searcher.close()
```

### Advanced Function Features
```python
from functools import wraps, lru_cache, singledispatch, partial
from typing import Callable, Any, TypeVar, Generic

# Function annotations and type hints
def process_data(data: list[dict], 
                transform: Callable[[dict], dict],
                filter_func: Callable[[dict], bool] = None) -> list[dict]:
    """Process data with transformation and optional filtering."""
    result = [transform(item) for item in data]
    if filter_func:
        result = [item for item in result if filter_func(item)]
    return result

# Closures and nonlocal
def create_counter(start: int = 0):
    """Create a counter function with closure."""
    count = start
    
    def counter(increment: int = 1):
        nonlocal count
        count += increment
        return count
    
    def reset():
        nonlocal count
        count = start
    
    counter.reset = reset
    return counter

# Function factory
def create_validator(min_val: float = None, max_val: float = None):
    """Create a validation function."""
    def validator(value: float) -> bool:
        if min_val is not None and value < min_val:
            return False
        if max_val is not None and value > max_val:
            return False
        return True
    
    return validator

# Advanced decorator with parameters
def retry(max_attempts: int = 3, delay: float = 1.0, 
          exceptions: tuple = (Exception,)):
    """Retry decorator with configurable parameters."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
                    continue
            raise last_exception
        return wrapper
    return decorator

# Single dispatch (method overloading)
@singledispatch
def process_item(item):
    """Generic item processor."""
    raise NotImplementedError(f"Cannot process {type(item)}")

@process_item.register
def _(item: str):
    return item.upper()

@process_item.register
def _(item: int):
    return item * 2

@process_item.register
def _(item: list):
    return [process_item(x) for x in item]

# Partial application
def power(base: float, exponent: float) -> float:
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5))  # 25
print(cube(3))    # 27
```

## Object-Oriented Programming {#oop}

### Advanced Class Features
```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import ClassVar, Protocol

# Abstract base classes
class Shape(ABC):
    """Abstract shape class."""
    
    @abstractmethod
    def area(self) -> float:
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        pass
    
    def describe(self) -> str:
        return f"{self.__class__.__name__}: Area={self.area():.2f}, Perimeter={self.perimeter():.2f}"

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height
    
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

# Dataclasses
@dataclass
class Point:
    x: float
    y: float
    z: float = 0.0
    
    def distance_from_origin(self) -> float:
        return (self.x**2 + self.y**2 + self.z**2)**0.5

@dataclass
class Person:
    name: str
    age: int
    email: str = ""
    skills: list[str] = field(default_factory=list)
    _id: int = field(default_factory=lambda: id(object()))
    
    def __post_init__(self):
        if not self.email:
            self.email = f"{self.name.lower().replace(' ', '.')}@example.com"

# Property decorators and descriptors
class Temperature:
    def __init__(self, celsius: float = 0):
        self._celsius = celsius
    
    @property
    def celsius(self) -> float:
        return self._celsius
    
    @celsius.setter
    def celsius(self, value: float):
        if value < -273.15:
            raise ValueError("Temperature cannot be below absolute zero")
        self._celsius = value
    
    @property
    def fahrenheit(self) -> float:
        return (self._celsius * 9/5) + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value: float):
        self.celsius = (value - 32) * 5/9
    
    @property
    def kelvin(self) -> float:
        return self._celsius + 273.15

# Class and static methods
class MathUtils:
    PI: ClassVar[float] = 3.14159
    
    def __init__(self, precision: int = 2):
        self.precision = precision
    
    @classmethod
    def create_high_precision(cls):
        """Factory method for high precision instance."""
        return cls(precision=10)
    
    @staticmethod
    def is_prime(n: int) -> bool:
        """Check if number is prime."""
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    def circle_area(self, radius: float) -> float:
        area = self.PI * radius**2
        return round(area, self.precision)

# Multiple inheritance and MRO
class Flyable:
    def fly(self):
        return "Flying"

class Swimmable:
    def swim(self):
        return "Swimming"

class Duck(Flyable, Swimmable):
    def __init__(self, name: str):
        self.name = name
    
    def speak(self):
        return "Quack"

# Method Resolution Order
print(Duck.__mro__)
duck = Duck("Donald")
print(duck.fly(), duck.swim(), duck.speak())
```

### Metaclasses and Advanced Features
```python
# Basic metaclass
class SingletonMeta(type):
    """Metaclass that creates singleton instances."""
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self, connection_string: str = "default"):
        self.connection_string = connection_string
        self.connected = False
    
    def connect(self):
        self.connected = True
        return f"Connected to {self.connection_string}"

# Attribute validation metaclass
class ValidatedMeta(type):
    def __new__(cls, name, bases, attrs):
        # Add validation to all methods
        for key, value in attrs.items():
            if callable(value) and not key.startswith('_'):
                attrs[key] = cls._add_validation(value)
        return super().__new__(cls, name, bases, attrs)
    
    @staticmethod
    def _add_validation(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Pre-execution validation
            if hasattr(self, '_validate'):
                self._validate()
            return func(self, *args, **kwargs)
        return wrapper

# Descriptor for attribute validation
class ValidatedAttribute:
    def __init__(self, validator_func, error_message="Invalid value"):
        self.validator = validator_func
        self.error_message = error_message
        self.private_name = None
    
    def __set_name__(self, owner, name):
        self.private_name = f'_{name}'
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)
    
    def __set__(self, obj, value):
        if not self.validator(value):
            raise ValueError(self.error_message)
        setattr(obj, self.private_name, value)

class Person:
    name = ValidatedAttribute(
        lambda x: isinstance(x, str) and len(x) > 0,
        "Name must be non-empty string"
    )
    age = ValidatedAttribute(
        lambda x: isinstance(x, int) and 0 <= x <= 150,
        "Age must be integer between 0 and 150"
    )
    
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

# Protocol (structural typing)
class Drawable(Protocol):
    def draw(self) -> str: ...

class Circle:
    def __init__(self, radius: float):
        self.radius = radius
    
    def draw(self) -> str:
        return f"Drawing circle with radius {self.radius}"

def render_shape(shape: Drawable) -> str:
    return shape.draw()

circle = Circle(5)
print(render_shape(circle))  # Works due to structural typing
```

## Decorators and Context Managers {#decorators}

### Advanced Decorators
```python
import functools
import time
from typing import Callable, Any

# Class-based decorator
class RateLimiter:
    def __init__(self, max_calls: int, time_window: int):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = []
    
    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # Remove old calls outside time window
            self.calls = [call_time for call_time in self.calls 
                         if now - call_time < self.time_window]
            
            if len(self.calls) >= self.max_calls:
                raise Exception(f"Rate limit exceeded: {self.max_calls} calls per {self.time_window}s")
            
            self.calls.append(now)
            return func(*args, **kwargs)
        
        return wrapper

# Decorator with state
class CallCounter:
    def __init__(self, func: Callable):
        self.func = func
        self.count = 0
        functools.update_wrapper(self, func)
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"Call #{self.count} to {self.func.__name__}")
        return self.func(*args, **kwargs)
    
    def reset(self):
        self.count = 0

# Decorator factory with complex logic
def memoize_with_ttl(ttl_seconds: int = 300):
    """Memoization with time-to-live."""
    def decorator(func: Callable) -> Callable:
        cache = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key
            key = str(args) + str(sorted(kwargs.items()))
            now = time.time()
            
            # Check if cached result exists and is still valid
            if key in cache:
                result, timestamp = cache[key]
                if now - timestamp < ttl_seconds:
                    return result
                else:
                    del cache[key]
            
            # Calculate and cache result
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result
        
        wrapper.cache_clear = cache.clear
        wrapper.cache_info = lambda: f"Cache size: {len(cache)}"
        return wrapper
    
    return decorator

# Usage examples
@RateLimiter(max_calls=5, time_window=60)
def api_call(data):
    return f"Processing {data}"

@CallCounter
def greet(name):
    return f"Hello, {name}!"

@memoize_with_ttl(ttl_seconds=10)
def expensive_calculation(n):
    time.sleep(1)  # Simulate expensive operation
    return n ** 2
```

### Context Managers
```python
import contextlib
import tempfile
import os
from typing import Generator

# Class-based context manager
class DatabaseTransaction:
    def __init__(self, connection):
        self.connection = connection
        self.transaction = None
    
    def __enter__(self):
        self.transaction = self.connection.begin()
        return self.transaction
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.transaction.commit()
        else:
            self.transaction.rollback()
        return False  # Don't suppress exceptions

# Function-based context manager
@contextlib.contextmanager
def temporary_directory() -> Generator[str, None, None]:
    """Create and cleanup temporary directory."""
    temp_dir = tempfile.mkdtemp()
    try:
        yield temp_dir
    finally:
        import shutil
        shutil.rmtree(temp_dir)

@contextlib.contextmanager
def timer(description: str = "Operation") -> Generator[None, None, None]:
    """Time the execution of a code block."""
    start_time = time.time()
    try:
        yield
    finally:
        elapsed = time.time() - start_time
        print(f"{description} took {elapsed:.4f} seconds")

@contextlib.contextmanager
def suppress_stdout():
    """Suppress stdout temporarily."""
    import sys
    original_stdout = sys.stdout
    try:
        sys.stdout = open(os.devnull, 'w')
        yield
    finally:
        sys.stdout.close()
        sys.stdout = original_stdout

# Multiple context managers
@contextlib.contextmanager
def file_manager(filename: str, backup: bool = True):
    """Manage file with optional backup."""
    backup_name = f"{filename}.backup" if backup else None
    
    # Create backup if requested
    if backup and os.path.exists(filename):
        import shutil
        shutil.copy2(filename, backup_name)
    
    try:
        with open(filename, 'w') as f:
            yield f
    except Exception:
        # Restore backup on error
        if backup_name and os.path.exists(backup_name):
            import shutil
            shutil.move(backup_name, filename)
        raise
    else:
        # Remove backup on success
        if backup_name and os.path.exists(backup_name):
            os.remove(backup_name)

# Usage examples
with temporary_directory() as temp_dir:
    print(f"Working in {temp_dir}")
    # Do work in temporary directory

with timer("Database query"):
    time.sleep(0.1)  # Simulate database operation

with file_manager("config.txt", backup=True) as f:
    f.write("new configuration")
```

## Concurrency and Parallelism {#concurrency}

### Threading
```python
import threading
import queue
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock, RLock, Semaphore, Event, Condition

# Thread-safe counter
class ThreadSafeCounter:
    def __init__(self):
        self._value = 0
        self._lock = Lock()
    
    def increment(self):
        with self._lock:
            self._value += 1
    
    def decrement(self):
        with self._lock:
            self._value -= 1
    
    @property
    def value(self):
        with self._lock:
            return self._value

# Producer-Consumer pattern
class ProducerConsumer:
    def __init__(self, max_size: int = 10):
        self.queue = queue.Queue(maxsize=max_size)
        self.shutdown = threading.Event()
    
    def producer(self, items: list):
        """Produce items and add to queue."""
        for item in items:
            if self.shutdown.is_set():
                break
            self.queue.put(item)
            print(f"Produced: {item}")
            time.sleep(0.1)
        
        # Signal end of production
        self.queue.put(None)
    
    def consumer(self, worker_id: int):
        """Consume items from queue."""
        while not self.shutdown.is_set():
            try:
                item = self.queue.get(timeout=1)
                if item is None:  # End signal
                    break
                
                print(f"Consumer {worker_id} processing: {item}")
                time.sleep(0.2)  # Simulate processing
                self.queue.task_done()
                
            except queue.Empty:
                continue
    
    def run(self, items: list, num_consumers: int = 3):
        """Run producer-consumer system."""
        threads = []
        
        # Start producer
        producer_thread = threading.Thread(
            target=self.producer, 
            args=(items,)
        )
        threads.append(producer_thread)
        producer_thread.start()
        
        # Start consumers
        for i in range(num_consumers):
            consumer_thread = threading.Thread(
                target=self.consumer,
                args=(i,)
            )
            threads.append(consumer_thread)
            consumer_thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join()

# Thread pool example
def process_data(data):
    """Simulate data processing."""
    result = sum(x**2 for x in data)
    time.sleep(0.1)
    return result

def parallel_processing(datasets: list):
    """Process multiple datasets in parallel."""
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit all tasks
        future_to_data = {
            executor.submit(process_data, data): data 
            for data in datasets
        }
        
        # Collect results as they complete
        results = []
        for future in as_completed(future_to_data):
            data = future_to_data[future]
            try:
                result = future.result()
                results.append((data, result))
            except Exception as exc:
                print(f"Data {data} generated exception: {exc}")
        
        return results
```

### Asyncio
```python
import asyncio
import aiohttp
import aiofiles
from typing import List, Dict, Any

# Basic async functions
async def fetch_url(session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
    """Fetch URL asynchronously."""
    try:
        async with session.get(url) as response:
            return {
                'url': url,
                'status': response.status,
                'content': await response.text()
            }
    except Exception as e:
        return {
            'url': url,
            'error': str(e)
        }

async def fetch_multiple_urls(urls: List[str]) -> List[Dict[str, Any]]:
    """Fetch multiple URLs concurrently."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return results

# Async file operations
async def process_file_async(file_path: str) -> int:
    """Process file asynchronously."""
    async with aiofiles.open(file_path, 'r') as file:
        content = await file.read()
        # Simulate processing
        await asyncio.sleep(0.1)
        return len(content.split())

async def process_multiple_files(file_paths: List[str]) -> Dict[str, int]:
    """Process multiple files concurrently."""
    tasks = [process_file_async(path) for path in file_paths]
    results = await asyncio.gather(*tasks)
    return dict(zip(file_paths, results))

# Async context manager
class AsyncDatabaseConnection:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connection = None
    
    async def __aenter__(self):
        # Simulate async connection
        await asyncio.sleep(0.1)
        self.connection = f"Connected to {self.connection_string}"
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Simulate async cleanup
        await asyncio.sleep(0.1)
        self.connection = None
    
    async def execute(self, query: str):
        await asyncio.sleep(0.05)  # Simulate query execution
        return f"Executed: {query}"

# Producer-Consumer with asyncio
class AsyncQueue:
    def __init__(self, maxsize: int = 0):
        self.queue = asyncio.Queue(maxsize=maxsize)
        self.active_producers = 0
        self.lock = asyncio.Lock()
    
    async def producer(self, items: List[Any], producer_id: int):
        """Produce items asynchronously."""
        async with self.lock:
            self.active_producers += 1
        
        try:
            for item in items:
                await self.queue.put((producer_id, item))
                print(f"Producer {producer_id} produced: {item}")
                await asyncio.sleep(0.1)
        finally:
            async with self.lock:
                self.active_producers -= 1
                if self.active_producers == 0:
                    await self.queue.put(None)  # End signal
    
    async def consumer(self, consumer_id: int):
        """Consume items asynchronously."""
        while True:
            item = await self.queue.get()
            if item is None:
                # Re-queue end signal for other consumers
                await self.queue.put(None)
                break
            
            producer_id, data = item
            print(f"Consumer {consumer_id} processing {data} from producer {producer_id}")
            await asyncio.sleep(0.2)  # Simulate processing
    
    async def run(self, producer_data: List[List[Any]], num_consumers: int = 2):
        """Run async producer-consumer system."""
        # Start producers
        producer_tasks = [
            asyncio.create_task(self.producer(data, i))
            for i, data in enumerate(producer_data)
        ]
        
        # Start consumers
        consumer_tasks = [
            asyncio.create_task(self.consumer(i))
            for i in range(num_consumers)
        ]
        
        # Wait for all tasks
        await asyncio.gather(*producer_tasks, *consumer_tasks)

# Usage example
async def main():
    # Fetch URLs
    urls = [
        "https://httpbin.org/get",
        "https://httpbin.org/headers",
        "https://httpbin.org/ip"
    ]
    
    results = await fetch_multiple_urls(urls)
    print(f"Fetched {len(results)} URLs")
    
    # Database operations
    async with AsyncDatabaseConnection("postgresql://localhost") as db:
        result = await db.execute("SELECT * FROM users")
        print(result)
    
    # Producer-Consumer
    queue_system = AsyncQueue()
    producer_data = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    await queue_system.run(producer_data, num_consumers=2)

# Run the async code
if __name__ == "__main__":
    asyncio.run(main())
```

This deep dive into Python covers advanced concepts that separate intermediate programmers from experts. Mastering these concepts will help you write more efficient, maintainable, and pythonic code.''',
            'category': 'Python',
            'tags': 'python,advanced,concurrency,metaprogramming',
        },
        {
            'title': 'TypeScript Enterprise Patterns',
            'content': '''# TypeScript Enterprise Patterns: Building Scalable Applications

## Table of Contents
1. [Introduction to Enterprise TypeScript](#introduction)
2. [Advanced Type System Features](#type-system)
3. [Design Patterns for TypeScript](#design-patterns)
4. [Dependency Injection and IoC](#dependency-injection)
5. [Domain-Driven Design with TypeScript](#ddd)
6. [Testing Strategies](#testing)
7. [Performance and Optimization](#performance)
8. [Error Handling and Logging](#error-handling)
9. [Configuration Management](#configuration)
10. [Production Best Practices](#production)

## Introduction to Enterprise TypeScript {#introduction}

Enterprise TypeScript development requires robust patterns, maintainable architectures, and scalable solutions. This guide explores advanced TypeScript patterns specifically designed for large-scale applications.

### Why TypeScript for Enterprise?
- **Type Safety**: Catch errors at compile time
- **Better IDE Support**: Enhanced IntelliSense and refactoring
- **Scalability**: Maintain large codebases with confidence
- **Team Productivity**: Clear contracts and interfaces
- **Gradual Adoption**: Can be introduced incrementally

### Project Structure for Enterprise
```typescript
src/
├── application/          # Application layer
│   ├── commands/        # Command handlers
│   ├── queries/         # Query handlers
│   └── services/        # Application services
├── domain/              # Domain layer
│   ├── entities/        # Domain entities
│   ├── repositories/    # Repository interfaces
│   ├── services/        # Domain services
│   └── value-objects/   # Value objects
├── infrastructure/      # Infrastructure layer
│   ├── database/        # Database implementations
│   ├── external/        # External service clients
│   └── repositories/    # Repository implementations
├── presentation/        # Presentation layer
│   ├── controllers/     # API controllers
│   ├── middleware/      # Express middleware
│   └── validators/      # Input validation
├── shared/              # Shared utilities
│   ├── decorators/      # Custom decorators
│   ├── types/           # Shared type definitions
│   └── utils/           # Utility functions
└── config/              # Configuration files
```

### Enterprise TypeScript Configuration
```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020", "DOM"],
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "experimentalDecorators": true,
    "emitDecoratorMetadata": true,
    "strictPropertyInitialization": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "resolveJsonModule": true,
    "baseUrl": "./src",
    "paths": {
      "@/*": ["*"],
      "@/domain/*": ["domain/*"],
      "@/application/*": ["application/*"],
      "@/infrastructure/*": ["infrastructure/*"]
    }
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

## Advanced Type System Features {#type-system}

### Conditional Types and Advanced Generics
```typescript
// Conditional types for API responses
type ApiResponse<T> = T extends string
  ? { message: T }
  : T extends object
  ? { data: T; meta: ResponseMeta }
  : never;

// Advanced utility types
type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

type RequiredKeys<T> = {
  [K in keyof T]-?: {} extends Pick<T, K> ? never : K;
}[keyof T];

type OptionalKeys<T> = {
  [K in keyof T]-?: {} extends Pick<T, K> ? K : never;
}[keyof T];

// Example usage
interface User {
  id: string;
  name: string;
  email?: string;
  preferences?: UserPreferences;
}

type RequiredUserKeys = RequiredKeys<User>; // "id" | "name"
type OptionalUserKeys = OptionalKeys<User>; // "email" | "preferences"
```

### Template Literal Types
```typescript
// Event system with template literals
type EventType = 'user' | 'order' | 'product';
type ActionType = 'created' | 'updated' | 'deleted';
type EventName = `${EventType}:${ActionType}`;

// Type-safe event emitter
interface EventMap {
  'user:created': { userId: string; timestamp: Date };
  'user:updated': { userId: string; changes: Partial<User> };
  'user:deleted': { userId: string };
  'order:created': { orderId: string; userId: string; amount: number };
  'order:updated': { orderId: string; changes: Partial<Order> };
  'order:deleted': { orderId: string };
}

class TypedEventEmitter {
  private listeners: {
    [K in keyof EventMap]?: Array<(data: EventMap[K]) => void>;
  } = {};

  on<K extends keyof EventMap>(
    event: K,
    listener: (data: EventMap[K]) => void
  ): void {
    if (!this.listeners[event]) {
      this.listeners[event] = [];
    }
    this.listeners[event]!.push(listener);
  }

  emit<K extends keyof EventMap>(event: K, data: EventMap[K]): void {
    const eventListeners = this.listeners[event];
    if (eventListeners) {
      eventListeners.forEach(listener => listener(data));
    }
  }
}

// Usage
const emitter = new TypedEventEmitter();
emitter.on('user:created', (data) => {
  // data is properly typed as { userId: string; timestamp: Date }
  console.log(`User ${data.userId} created at ${data.timestamp}`);
});
```

### Branded Types for Domain Modeling
```typescript
// Branded types for type safety
type Brand<T, B> = T & { __brand: B };

type UserId = Brand<string, 'UserId'>;
type Email = Brand<string, 'Email'>;
type OrderId = Brand<string, 'OrderId'>;
type Money = Brand<number, 'Money'>;

// Factory functions for branded types
const createUserId = (id: string): UserId => {
  if (!id || id.length < 1) {
    throw new Error('Invalid user ID');
  }
  return id as UserId;
};

const createEmail = (email: string): Email => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    throw new Error('Invalid email format');
  }
  return email as Email;
};

const createMoney = (amount: number): Money => {
  if (amount < 0 || !Number.isFinite(amount)) {
    throw new Error('Invalid money amount');
  }
  return Math.round(amount * 100) / 100 as Money;
};

// Domain entities with branded types
interface User {
  readonly id: UserId;
  readonly email: Email;
  name: string;
  createdAt: Date;
}

interface Order {
  readonly id: OrderId;
  readonly userId: UserId;
  amount: Money;
  status: OrderStatus;
}
```

### Advanced Mapped Types
```typescript
// Create immutable versions of types
type Immutable<T> = {
  readonly [K in keyof T]: T[K] extends object ? Immutable<T[K]> : T[K];
};

// Create mutable versions of readonly types
type Mutable<T> = {
  -readonly [K in keyof T]: T[K] extends object ? Mutable<T[K]> : T[K];
};

// Extract function property names
type FunctionPropertyNames<T> = {
  [K in keyof T]: T[K] extends Function ? K : never;
}[keyof T];

type FunctionProperties<T> = Pick<T, FunctionPropertyNames<T>>;

// Example: Service interface extraction
interface UserService {
  findById(id: UserId): Promise<User | null>;
  create(userData: CreateUserData): Promise<User>;
  update(id: UserId, data: Partial<User>): Promise<User>;
  delete(id: UserId): Promise<void>;
  validateEmail(email: string): boolean;
}

type UserServiceMethods = FunctionProperties<UserService>;
// Result: all method signatures from UserService
```

## Design Patterns for TypeScript {#design-patterns}

### Repository Pattern with Generics
```typescript
// Generic repository interface
interface Repository<T, ID> {
  findById(id: ID): Promise<T | null>;
  findAll(criteria?: Partial<T>): Promise<T[]>;
  save(entity: T): Promise<T>;
  update(id: ID, updates: Partial<T>): Promise<T>;
  delete(id: ID): Promise<void>;
  exists(id: ID): Promise<boolean>;
}

// Base repository implementation
abstract class BaseRepository<T, ID> implements Repository<T, ID> {
  protected abstract tableName: string;
  
  async findById(id: ID): Promise<T | null> {
    // Generic implementation
    const result = await this.executeQuery(
      `SELECT * FROM ${this.tableName} WHERE id = ?`,
      [id]
    );
    return result.length > 0 ? this.mapToEntity(result[0]) : null;
  }

  async findAll(criteria?: Partial<T>): Promise<T[]> {
    const whereClause = this.buildWhereClause(criteria);
    const query = `SELECT * FROM ${this.tableName}${whereClause}`;
    const results = await this.executeQuery(query);
    return results.map(row => this.mapToEntity(row));
  }

  async save(entity: T): Promise<T> {
    const fields = this.getEntityFields(entity);
    const placeholders = fields.map(() => '?').join(', ');
    const query = `INSERT INTO ${this.tableName} (${fields.join(', ')}) VALUES (${placeholders})`;
    const values = fields.map(field => (entity as any)[field]);
    
    const result = await this.executeQuery(query, values);
    return { ...entity, id: result.insertId } as T;
  }

  protected abstract executeQuery(query: string, params?: any[]): Promise<any>;
  protected abstract mapToEntity(row: any): T;
  protected abstract getEntityFields(entity: T): string[];
  protected abstract buildWhereClause(criteria?: Partial<T>): string;
}

// Concrete repository implementation
class UserRepository extends BaseRepository<User, UserId> {
  protected tableName = 'users';

  protected async executeQuery(query: string, params?: any[]): Promise<any> {
    // Database-specific implementation
    return await this.database.execute(query, params);
  }

  protected mapToEntity(row: any): User {
    return {
      id: createUserId(row.id),
      email: createEmail(row.email),
      name: row.name,
      createdAt: new Date(row.created_at)
    };
  }

  protected getEntityFields(entity: User): string[] {
    return ['email', 'name', 'created_at'];
  }

  protected buildWhereClause(criteria?: Partial<User>): string {
    if (!criteria) return '';
    
    const conditions = Object.entries(criteria)
      .filter(([_, value]) => value !== undefined)
      .map(([key, _]) => `${key} = ?`);
    
    return conditions.length > 0 ? ` WHERE ${conditions.join(' AND ')}` : '';
  }

  // Domain-specific methods
  async findByEmail(email: Email): Promise<User | null> {
    const result = await this.executeQuery(
      `SELECT * FROM ${this.tableName} WHERE email = ?`,
      [email]
    );
    return result.length > 0 ? this.mapToEntity(result[0]) : null;
  }
}
```

### Factory Pattern with Type Safety
```typescript
// Abstract factory for creating domain objects
abstract class EntityFactory<T> {
  abstract create(data: unknown): T;
  abstract validate(data: unknown): data is T;
}

// User factory implementation
interface CreateUserData {
  email: string;
  name: string;
}

class UserFactory extends EntityFactory<User> {
  create(data: CreateUserData): User {
    if (!this.validate(data)) {
      throw new Error('Invalid user data');
    }

    return {
      id: createUserId(this.generateId()),
      email: createEmail(data.email),
      name: data.name.trim(),
      createdAt: new Date()
    };
  }

  validate(data: unknown): data is CreateUserData {
    if (typeof data !== 'object' || data === null) {
      return false;
    }

    const candidate = data as Record<string, unknown>;
    return (
      typeof candidate.email === 'string' &&
      typeof candidate.name === 'string' &&
      this.isValidEmail(candidate.email) &&
      candidate.name.trim().length > 0
    );
  }

  private isValidEmail(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  private generateId(): string {
    return `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}

// Factory registry for different entity types
class FactoryRegistry {
  private factories = new Map<string, EntityFactory<any>>();

  register<T>(type: string, factory: EntityFactory<T>): void {
    this.factories.set(type, factory);
  }

  create<T>(type: string, data: unknown): T {
    const factory = this.factories.get(type);
    if (!factory) {
      throw new Error(`No factory registered for type: ${type}`);
    }
    return factory.create(data);
  }
}

// Usage
const factoryRegistry = new FactoryRegistry();
factoryRegistry.register('user', new UserFactory());

const user = factoryRegistry.create<User>('user', {
  email: 'john@example.com',
  name: 'John Doe'
});
```

### Command Pattern with CQRS
```typescript
// Command interfaces
interface Command {
  readonly type: string;
  readonly timestamp: Date;
}

interface CommandHandler<T extends Command> {
  handle(command: T): Promise<void>;
}

// Query interfaces
interface Query<TResult> {
  readonly type: string;
}

interface QueryHandler<TQuery extends Query<TResult>, TResult> {
  handle(query: TQuery): Promise<TResult>;
}

// Command implementations
class CreateUserCommand implements Command {
  readonly type = 'CreateUser';
  readonly timestamp = new Date();

  constructor(
    public readonly userData: CreateUserData,
    public readonly requestId: string
  ) {}
}

class UpdateUserCommand implements Command {
  readonly type = 'UpdateUser';
  readonly timestamp = new Date();

  constructor(
    public readonly userId: UserId,
    public readonly updates: Partial<User>,
    public readonly requestId: string
  ) {}
}

// Command handlers
class CreateUserCommandHandler implements CommandHandler<CreateUserCommand> {
  constructor(
    private userRepository: UserRepository,
    private userFactory: UserFactory,
    private eventBus: EventBus
  ) {}

  async handle(command: CreateUserCommand): Promise<void> {
    // Check if user already exists
    const existingUser = await this.userRepository.findByEmail(
      createEmail(command.userData.email)
    );
    
    if (existingUser) {
      throw new DomainError('User with this email already exists');
    }

    // Create new user
    const user = this.userFactory.create(command.userData);
    await this.userRepository.save(user);

    // Publish domain event
    await this.eventBus.publish(new UserCreatedEvent(user.id, command.timestamp));
  }
}

// Query implementations
class GetUserByIdQuery implements Query<User | null> {
  readonly type = 'GetUserById';

  constructor(public readonly userId: UserId) {}
}

class GetUsersQuery implements Query<User[]> {
  readonly type = 'GetUsers';

  constructor(
    public readonly filters?: UserFilters,
    public readonly pagination?: PaginationOptions
  ) {}
}

// Query handlers
class GetUserByIdQueryHandler implements QueryHandler<GetUserByIdQuery, User | null> {
  constructor(private userRepository: UserRepository) {}

  async handle(query: GetUserByIdQuery): Promise<User | null> {
    return await this.userRepository.findById(query.userId);
  }
}

// Command/Query bus
class Bus {
  private commandHandlers = new Map<string, CommandHandler<any>>();
  private queryHandlers = new Map<string, QueryHandler<any, any>>();

  registerCommandHandler<T extends Command>(
    commandType: string,
    handler: CommandHandler<T>
  ): void {
    this.commandHandlers.set(commandType, handler);
  }

  registerQueryHandler<TQuery extends Query<TResult>, TResult>(
    queryType: string,
    handler: QueryHandler<TQuery, TResult>
  ): void {
    this.queryHandlers.set(queryType, handler);
  }

  async executeCommand<T extends Command>(command: T): Promise<void> {
    const handler = this.commandHandlers.get(command.type);
    if (!handler) {
      throw new Error(`No handler registered for command: ${command.type}`);
    }
    await handler.handle(command);
  }

  async executeQuery<TResult>(query: Query<TResult>): Promise<TResult> {
    const handler = this.queryHandlers.get(query.type);
    if (!handler) {
      throw new Error(`No handler registered for query: ${query.type}`);
    }
    return await handler.handle(query);
  }
}
```

## Dependency Injection and IoC {#dependency-injection}

### Custom Dependency Injection Container
```typescript
// Service registration types
type ServiceFactory<T> = () => T;
type ServiceConstructor<T> = new (...args: any[]) => T;
type ServiceLifetime = 'singleton' | 'transient' | 'scoped';

interface ServiceRegistration<T> {
  lifetime: ServiceLifetime;
  factory?: ServiceFactory<T>;
  constructor?: ServiceConstructor<T>;
  dependencies?: string[];
}

// IoC Container implementation
class Container {
  private services = new Map<string, ServiceRegistration<any>>();
  private singletons = new Map<string, any>();
  private scoped = new Map<string, any>();

  register<T>(
    name: string,
    registration: ServiceRegistration<T>
  ): void {
    this.services.set(name, registration);
  }

  registerSingleton<T>(
    name: string,
    factory: ServiceFactory<T>
  ): void {
    this.register(name, { lifetime: 'singleton', factory });
  }

  registerTransient<T>(
    name: string,
    constructor: ServiceConstructor<T>,
    dependencies: string[] = []
  ): void {
    this.register(name, {
      lifetime: 'transient',
      constructor,
      dependencies
    });
  }

  resolve<T>(name: string): T {
    const registration = this.services.get(name);
    if (!registration) {
      throw new Error(`Service not registered: ${name}`);
    }

    switch (registration.lifetime) {
      case 'singleton':
        return this.resolveSingleton<T>(name, registration);
      case 'transient':
        return this.resolveTransient<T>(registration);
      case 'scoped':
        return this.resolveScoped<T>(name, registration);
      default:
        throw new Error(`Unknown service lifetime: ${registration.lifetime}`);
    }
  }

  private resolveSingleton<T>(
    name: string,
    registration: ServiceRegistration<T>
  ): T {
    if (this.singletons.has(name)) {
      return this.singletons.get(name);
    }

    const instance = this.createInstance<T>(registration);
    this.singletons.set(name, instance);
    return instance;
  }

  private resolveTransient<T>(registration: ServiceRegistration<T>): T {
    return this.createInstance<T>(registration);
  }

  private resolveScoped<T>(
    name: string,
    registration: ServiceRegistration<T>
  ): T {
    if (this.scoped.has(name)) {
      return this.scoped.get(name);
    }

    const instance = this.createInstance<T>(registration);
    this.scoped.set(name, instance);
    return instance;
  }

  private createInstance<T>(registration: ServiceRegistration<T>): T {
    if (registration.factory) {
      return registration.factory();
    }

    if (registration.constructor) {
      const dependencies = (registration.dependencies || []).map(dep =>
        this.resolve(dep)
      );
      return new registration.constructor(...dependencies);
    }

    throw new Error('No factory or constructor provided for service');
  }

  clearScoped(): void {
    this.scoped.clear();
  }
}

// Service decorators
const Injectable = (name: string, dependencies: string[] = []) => {
  return <T extends new (...args: any[]) => {}>(constructor: T) => {
    // Store metadata for automatic registration
    Reflect.defineMetadata('injectable', { name, dependencies }, constructor);
    return constructor;
  };
};

// Example service implementations
interface ILogger {
  log(message: string): void;
  error(message: string, error?: Error): void;
}

@Injectable('logger')
class ConsoleLogger implements ILogger {
  log(message: string): void {
    console.log(`[LOG] ${new Date().toISOString()}: ${message}`);
  }

  error(message: string, error?: Error): void {
    console.error(`[ERROR] ${new Date().toISOString()}: ${message}`, error);
  }
}

interface IUserRepository {
  findById(id: UserId): Promise<User | null>;
  save(user: User): Promise<void>;
}

@Injectable('userRepository', ['database', 'logger'])
class UserRepositoryImpl implements IUserRepository {
  constructor(
    private database: Database,
    private logger: ILogger
  ) {}

  async findById(id: UserId): Promise<User | null> {
    this.logger.log(`Finding user by ID: ${id}`);
    // Implementation details...
    return null;
  }

  async save(user: User): Promise<void> {
    this.logger.log(`Saving user: ${user.id}`);
    // Implementation details...
  }
}

@Injectable('userService', ['userRepository', 'logger'])
class UserService {
  constructor(
    private userRepository: IUserRepository,
    private logger: ILogger
  ) {}

  async getUser(id: UserId): Promise<User | null> {
    this.logger.log(`Getting user: ${id}`);
    return await this.userRepository.findById(id);
  }
}

// Container setup
const container = new Container();

// Register services
container.registerSingleton('logger', () => new ConsoleLogger());
container.registerSingleton('database', () => new DatabaseImpl());
container.registerTransient('userRepository', UserRepositoryImpl, ['database', 'logger']);
container.registerTransient('userService', UserService, ['userRepository', 'logger']);

// Usage
const userService = container.resolve<UserService>('userService');
```

## Domain-Driven Design with TypeScript {#ddd}

### Value Objects and Entities
```typescript
// Base value object
abstract class ValueObject {
  protected abstract getAtomicValues(): any[];

  equals(other: ValueObject): boolean {
    if (this.constructor !== other.constructor) {
      return false;
    }

    const thisValues = this.getAtomicValues();
    const otherValues = other.getAtomicValues();

    if (thisValues.length !== otherValues.length) {
      return false;
    }

    return thisValues.every((value, index) => 
      this.areEqual(value, otherValues[index])
    );
  }

  private areEqual(a: any, b: any): boolean {
    if (a === null || a === undefined || b === null || b === undefined) {
      return a === b;
    }

    if (a instanceof ValueObject && b instanceof ValueObject) {
      return a.equals(b);
    }

    return a === b;
  }
}

// Example value objects
class Money extends ValueObject {
  private constructor(
    private readonly amount: number,
    private readonly currency: string
  ) {
    super();
    if (amount < 0) {
      throw new Error('Money amount cannot be negative');
    }
    if (!currency || currency.length !== 3) {
      throw new Error('Currency must be a 3-letter code');
    }
  }

  static create(amount: number, currency: string): Money {
    return new Money(amount, currency);
  }

  getAmount(): number {
    return this.amount;
  }

  getCurrency(): string {
    return this.currency;
  }

  add(other: Money): Money {
    if (this.currency !== other.currency) {
      throw new Error('Cannot add money with different currencies');
    }
    return new Money(this.amount + other.amount, this.currency);
  }

  multiply(factor: number): Money {
    return new Money(this.amount * factor, this.currency);
  }

  protected getAtomicValues(): any[] {
    return [this.amount, this.currency];
  }
}

class Address extends ValueObject {
  private constructor(
    private readonly street: string,
    private readonly city: string,
    private readonly postalCode: string,
    private readonly country: string
  ) {
    super();
    this.validate();
  }

  static create(street: string, city: string, postalCode: string, country: string): Address {
    return new Address(street, city, postalCode, country);
  }

  private validate(): void {
    if (!this.street?.trim()) {
      throw new Error('Street is required');
    }
    if (!this.city?.trim()) {
      throw new Error('City is required');
    }
    if (!this.postalCode?.trim()) {
      throw new Error('Postal code is required');
    }
    if (!this.country?.trim()) {
      throw new Error('Country is required');
    }
  }

  getFullAddress(): string {
    return `${this.street}, ${this.city} ${this.postalCode}, ${this.country}`;
  }

  protected getAtomicValues(): any[] {
    return [this.street, this.city, this.postalCode, this.country];
  }
}

// Base entity
abstract class Entity<T> {
  protected constructor(protected readonly id: T) {}

  getId(): T {
    return this.id;
  }

  equals(other: Entity<T>): boolean {
    if (this.constructor !== other.constructor) {
      return false;
    }
    return this.id === other.id;
  }
}

// Domain entities
class Customer extends Entity<CustomerId> {
  private constructor(
    id: CustomerId,
    private name: string,
    private email: Email,
    private address: Address,
    private readonly createdAt: Date = new Date()
  ) {
    super(id);
  }

  static create(name: string, email: Email, address: Address): Customer {
    const id = CustomerId.generate();
    return new Customer(id, name, email, address);
  }

  static reconstitute(
    id: CustomerId,
    name: string,
    email: Email,
    address: Address,
    createdAt: Date
  ): Customer {
    return new Customer(id, name, email, address, createdAt);
  }

  updateAddress(newAddress: Address): void {
    this.address = newAddress;
    // Publish domain event
    DomainEvents.publish(new CustomerAddressChangedEvent(this.id, newAddress));
  }

  getName(): string {
    return this.name;
  }

  getEmail(): Email {
    return this.email;
  }

  getAddress(): Address {
    return this.address;
  }

  getCreatedAt(): Date {
    return this.createdAt;
  }
}

// Aggregate root
class Order extends Entity<OrderId> {
  private items: OrderItem[] = [];
  private status: OrderStatus = OrderStatus.PENDING;

  private constructor(
    id: OrderId,
    private readonly customerId: CustomerId,
    private readonly createdAt: Date = new Date()
  ) {
    super(id);
  }

  static create(customerId: CustomerId): Order {
    const id = OrderId.generate();
    const order = new Order(id, customerId);
    
    // Publish domain event
    DomainEvents.publish(new OrderCreatedEvent(id, customerId));
    
    return order;
  }

  addItem(productId: ProductId, quantity: number, unitPrice: Money): void {
    if (this.status !== OrderStatus.PENDING) {
      throw new Error('Cannot modify confirmed order');
    }

    const existingItem = this.items.find(item => 
      item.getProductId().equals(productId)
    );

    if (existingItem) {
      existingItem.updateQuantity(existingItem.getQuantity() + quantity);
    } else {
      this.items.push(OrderItem.create(productId, quantity, unitPrice));
    }
  }

  removeItem(productId: ProductId): void {
    if (this.status !== OrderStatus.PENDING) {
      throw new Error('Cannot modify confirmed order');
    }

    this.items = this.items.filter(item => 
      !item.getProductId().equals(productId)
    );
  }

  confirm(): void {
    if (this.items.length === 0) {
      throw new Error('Cannot confirm order without items');
    }

    this.status = OrderStatus.CONFIRMED;
    DomainEvents.publish(new OrderConfirmedEvent(this.id, this.getTotalAmount()));
  }

  getTotalAmount(): Money {
    return this.items.reduce(
      (total, item) => total.add(item.getTotalPrice()),
      Money.create(0, 'USD')
    );
  }

  getItems(): readonly OrderItem[] {
    return [...this.items];
  }

  getStatus(): OrderStatus {
    return this.status;
  }
}
```

### Domain Events
```typescript
// Domain event infrastructure
interface DomainEvent {
  readonly eventId: string;
  readonly occurredOn: Date;
  readonly aggregateId: string;
  readonly eventType: string;
}

abstract class BaseDomainEvent implements DomainEvent {
  readonly eventId: string;
  readonly occurredOn: Date;

  constructor(public readonly aggregateId: string) {
    this.eventId = this.generateEventId();
    this.occurredOn = new Date();
  }

  abstract get eventType(): string;

  private generateEventId(): string {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
}

// Concrete domain events
class CustomerAddressChangedEvent extends BaseDomainEvent {
  readonly eventType = 'CustomerAddressChanged';

  constructor(
    customerId: CustomerId,
    public readonly newAddress: Address
  ) {
    super(customerId.toString());
  }
}

class OrderCreatedEvent extends BaseDomainEvent {
  readonly eventType = 'OrderCreated';

  constructor(
    orderId: OrderId,
    public readonly customerId: CustomerId
  ) {
    super(orderId.toString());
  }
}

class OrderConfirmedEvent extends BaseDomainEvent {
  readonly eventType = 'OrderConfirmed';

  constructor(
    orderId: OrderId,
    public readonly totalAmount: Money
  ) {
    super(orderId.toString());
  }
}

// Domain event dispatcher
type EventHandler<T extends DomainEvent> = (event: T) => Promise<void>;

class DomainEvents {
  private static handlers = new Map<string, EventHandler<any>[]>();
  private static pendingEvents: DomainEvent[] = [];

  static subscribe<T extends DomainEvent>(
    eventType: string,
    handler: EventHandler<T>
  ): void {
    if (!this.handlers.has(eventType)) {
      this.handlers.set(eventType, []);
    }
    this.handlers.get(eventType)!.push(handler);
  }

  static publish(event: DomainEvent): void {
    this.pendingEvents.push(event);
  }

  static async dispatchAll(): Promise<void> {
    const events = [...this.pendingEvents];
    this.pendingEvents.length = 0;

    for (const event of events) {
      await this.dispatch(event);
    }
  }

  private static async dispatch(event: DomainEvent): Promise<void> {
    const handlers = this.handlers.get(event.eventType) || [];
    
    for (const handler of handlers) {
      try {
        await handler(event);
      } catch (error) {
        console.error(`Error handling event ${event.eventType}:`, error);
        // In production, you'd want proper error handling/retry logic
      }
    }
  }

  static clear(): void {
    this.pendingEvents.length = 0;
  }
}

// Event handlers
class OrderCreatedEventHandler {
  constructor(
    private emailService: EmailService,
    private inventoryService: InventoryService
  ) {}

  async handle(event: OrderCreatedEvent): Promise<void> {
    // Send confirmation email
    await this.emailService.sendOrderCreatedEmail(event.customerId);
    
    // Reserve inventory
    await this.inventoryService.reserveForOrder(event.aggregateId);
  }
}

// Setup event handlers
DomainEvents.subscribe('OrderCreated', (event: OrderCreatedEvent) => 
  new OrderCreatedEventHandler(emailService, inventoryService).handle(event)
);
```

## Testing Strategies {#testing}

### Unit Testing with Jest and TypeScript
```typescript
// Test setup and utilities
import { describe, it, expect, beforeEach, jest } from '@jest/globals';

// Mock factory for creating test data
class TestDataBuilder {
  static createValidUser(): User {
    return {
      id: createUserId('test-user-123'),
      email: createEmail('test@example.com'),
      name: 'Test User',
      createdAt: new Date('2023-01-01T00:00:00Z')
    };
  }

  static createValidOrder(): Order {
    const customerId = CustomerId.generate();
    return Order.create(customerId);
  }

  static createMoney(amount: number = 100, currency: string = 'USD'): Money {
    return Money.create(amount, currency);
  }
}

// Mock implementations for dependencies
class MockUserRepository implements IUserRepository {
  private users = new Map<string, User>();

  async findById(id: UserId): Promise<User | null> {
    return this.users.get(id.toString()) || null;
  }

  async save(user: User): Promise<void> {
    this.users.set(user.getId().toString(), user);
  }

  async findByEmail(email: Email): Promise<User | null> {
    for (const user of this.users.values()) {
      if (user.getEmail() === email) {
        return user;
      }
    }
    return null;
  }

  // Test helper methods
  clear(): void {
    this.users.clear();
  }

  getStoredUsers(): User[] {
    return Array.from(this.users.values());
  }
}

// Unit tests for value objects
describe('Money', () => {
  describe('create', () => {
    it('should create money with valid amount and currency', () => {
      const money = Money.create(100, 'USD');
      
      expect(money.getAmount()).toBe(100);
      expect(money.getCurrency()).toBe('USD');
    });

    it('should throw error for negative amount', () => {
      expect(() => Money.create(-10, 'USD')).toThrow('Money amount cannot be negative');
    });

    it('should throw error for invalid currency', () => {
      expect(() => Money.create(100, 'US')).toThrow('Currency must be a 3-letter code');
    });
  });

  describe('add', () => {
    it('should add money with same currency', () => {
      const money1 = Money.create(100, 'USD');
      const money2 = Money.create(50, 'USD');
      
      const result = money1.add(money2);
      
      expect(result.getAmount()).toBe(150);
      expect(result.getCurrency()).toBe('USD');
    });

    it('should throw error when adding different currencies', () => {
      const usd = Money.create(100, 'USD');
      const eur = Money.create(50, 'EUR');
      
      expect(() => usd.add(eur)).toThrow('Cannot add money with different currencies');
    });
  });

  describe('equals', () => {
    it('should return true for equal money objects', () => {
      const money1 = Money.create(100, 'USD');
      const money2 = Money.create(100, 'USD');
      
      expect(money1.equals(money2)).toBe(true);
    });

    it('should return false for different amounts', () => {
      const money1 = Money.create(100, 'USD');
      const money2 = Money.create(50, 'USD');
      
      expect(money1.equals(money2)).toBe(false);
    });
  });
});

// Unit tests for entities
describe('Order', () => {
  let customerId: CustomerId;

  beforeEach(() => {
    customerId = CustomerId.generate();
  });

  describe('create', () => {
    it('should create order with pending status', () => {
      const order = Order.create(customerId);
      
      expect(order.getStatus()).toBe(OrderStatus.PENDING);
      expect(order.getItems()).toHaveLength(0);
    });
  });

  describe('addItem', () => {
    it('should add new item to order', () => {
      const order = Order.create(customerId);
      const productId = ProductId.generate();
      const unitPrice = Money.create(50, 'USD');
      
      order.addItem(productId, 2, unitPrice);
      
      expect(order.getItems()).toHaveLength(1);
      expect(order.getTotalAmount().getAmount()).toBe(100);
    });

    it('should increase quantity for existing item', () => {
      const order = Order.create(customerId);
      const productId = ProductId.generate();
      const unitPrice = Money.create(50, 'USD');
      
      order.addItem(productId, 2, unitPrice);
      order.addItem(productId, 1, unitPrice);
      
      expect(order.getItems()).toHaveLength(1);
      expect(order.getItems()[0]!.getQuantity()).toBe(3);
    });

    it('should throw error when adding to confirmed order', () => {
      const order = Order.create(customerId);
      const productId = ProductId.generate();
      const unitPrice = Money.create(50, 'USD');
      
      order.addItem(productId, 1, unitPrice);
      order.confirm();
      
      expect(() => order.addItem(productId, 1, unitPrice))
        .toThrow('Cannot modify confirmed order');
    });
  });

  describe('confirm', () => {
    it('should confirm order with items', () => {
      const order = Order.create(customerId);
      const productId = ProductId.generate();
      const unitPrice = Money.create(50, 'USD');
      
      order.addItem(productId, 1, unitPrice);
      order.confirm();
      
      expect(order.getStatus()).toBe(OrderStatus.CONFIRMED);
    });

    it('should throw error when confirming empty order', () => {
      const order = Order.create(customerId);
      
      expect(() => order.confirm()).toThrow('Cannot confirm order without items');
    });
  });
});

// Integration tests for services
describe('UserService', () => {
  let userService: UserService;
  let mockRepository: MockUserRepository;
  let mockLogger: jest.Mocked<ILogger>;

  beforeEach(() => {
    mockRepository = new MockUserRepository();
    mockLogger = {
      log: jest.fn(),
      error: jest.fn()
    };
    userService = new UserService(mockRepository, mockLogger);
  });

  describe('getUser', () => {
    it('should return user when found', async () => {
      const user = TestDataBuilder.createValidUser();
      await mockRepository.save(user);
      
      const result = await userService.getUser(user.getId());
      
      expect(result).toEqual(user);
      expect(mockLogger.log).toHaveBeenCalledWith(`Getting user: ${user.getId()}`);
    });

    it('should return null when user not found', async () => {
      const userId = createUserId('non-existent');
      
      const result = await userService.getUser(userId);
      
      expect(result).toBeNull();
    });
  });
});

// Test utilities for async operations
describe('AsyncTestUtils', () => {
  it('should handle domain events in tests', async () => {
    const events: DomainEvent[] = [];
    
    // Subscribe to events for testing
    DomainEvents.subscribe('OrderCreated', async (event) => {
      events.push(event);
    });

    const customerId = CustomerId.generate();
    Order.create(customerId);

    await DomainEvents.dispatchAll();

    expect(events).toHaveLength(1);
    expect(events[0]!.eventType).toBe('OrderCreated');
  });
});
```

This comprehensive guide covers the essential patterns and practices for building enterprise-grade TypeScript applications. The type system, design patterns, dependency injection, domain-driven design principles, and testing strategies shown here provide a solid foundation for scalable, maintainable applications.

Remember that enterprise development is about finding the right balance between flexibility and constraints, ensuring your codebase can evolve while maintaining reliability and performance. Use these patterns judiciously, applying them where they add value rather than complexity.''',
            'category': 'TypeScript',
            'tags': 'typescript,design-patterns,enterprise,testing',
        },
        {
            'title': 'Modern JavaScript Ecosystem',
            'content': '''# Modern JavaScript Ecosystem: Complete Developer Guide

## Table of Contents
1. [Evolution of JavaScript](#evolution)
2. [ECMAScript Features](#ecmascript)
3. [Node.js and Server-Side JavaScript](#nodejs)
4. [Package Management](#package-management)
5. [Build Tools and Bundlers](#build-tools)
6. [Testing Frameworks](#testing)
7. [Frontend Frameworks and Libraries](#frontend)
8. [Development Tools](#dev-tools)
9. [Performance and Optimization](#performance)
10. [Future of JavaScript](#future)

## Evolution of JavaScript {#evolution}

JavaScript has evolved from a simple scripting language for web pages to a powerful, versatile language that runs everywhere - from browsers and servers to mobile apps and desktop applications.

### Timeline of JavaScript
```javascript
// 1995: JavaScript created by Brendan Eich at Netscape
// 1997: ECMAScript standardization begins
// 2009: Node.js brings JavaScript to the server
// 2015: ES6/ES2015 - Major language overhaul
// 2020s: Modern JavaScript ecosystem maturity

// The evolution of variable declarations
// ES3 (1999)
var name = 'JavaScript';

// ES6 (2015)
const name = 'JavaScript';
let version = 'ES6';

// Modern features
const config = {
  name: 'Modern JavaScript',
  features: ['async/await', 'modules', 'classes', 'destructuring'],
  ecosystem: new Set(['Node.js', 'React', 'Vue', 'Angular'])
};
```

### JavaScript Everywhere
```javascript
// Browser (Frontend)
document.addEventListener('DOMContentLoaded', () => {
  console.log('JavaScript in the browser');
});

// Server (Node.js)
const express = require('express');
const app = express();
app.listen(3000, () => console.log('JavaScript on the server'));

// Mobile (React Native)
import { View, Text } from 'react-native';
const App = () => <View><Text>JavaScript on mobile</Text></View>;

// Desktop (Electron)
const { app, BrowserWindow } = require('electron');
const createWindow = () => {
  const win = new BrowserWindow({ width: 800, height: 600 });
  win.loadFile('index.html');
};

// IoT and Embedded (Johnny-Five)
const { Board, Led } = require('johnny-five');
const board = new Board();
board.on('ready', () => {
  const led = new Led(13);
  led.blink(500);
});
```

## ECMAScript Features {#ecmascript}

### ES6/ES2015 Foundation Features
```javascript
// Arrow Functions
const numbers = [1, 2, 3, 4, 5];

// Traditional function
const doubled = numbers.map(function(n) {
  return n * 2;
});

// Arrow function
const doubledArrow = numbers.map(n => n * 2);

// Complex arrow functions
const processUsers = users => users
  .filter(user => user.active)
  .map(user => ({
    id: user.id,
    name: user.name.toUpperCase(),
    email: user.email.toLowerCase()
  }))
  .sort((a, b) => a.name.localeCompare(b.name));

// Template Literals
const user = { name: 'Alice', age: 30 };
const greeting = `Hello, ${user.name}! You are ${user.age} years old.`;

// Multi-line strings
const htmlTemplate = `
  <div class="user-card">
    <h2>${user.name}</h2>
    <p>Age: ${user.age}</p>
    <p>Status: ${user.age >= 18 ? 'Adult' : 'Minor'}</p>
  </div>
`;

// Tagged template literals
function highlight(strings, ...values) {
  return strings.reduce((result, string, i) => {
    const value = values[i] ? `<mark>${values[i]}</mark>` : '';
    return result + string + value;
  }, '');
}

const searchTerm = 'JavaScript';
const text = highlight`Welcome to ${searchTerm} programming!`;

// Destructuring
const person = {
  name: 'Bob',
  age: 25,
  address: {
    street: '123 Main St',
    city: 'Anytown',
    country: 'USA'
  },
  hobbies: ['reading', 'coding', 'gaming']
};

// Object destructuring
const { name, age, address: { city } } = person;

// Array destructuring
const [firstHobby, secondHobby, ...otherHobbies] = person.hobbies;

// Function parameter destructuring
function createUser({ name, email, age = 18 }) {
  return {
    id: Date.now(),
    name,
    email,
    age,
    created: new Date()
  };
}

// Spread and Rest Operators
// Spread in arrays
const fruits = ['apple', 'banana'];
const moreFruits = ['orange', 'grape'];
const allFruits = [...fruits, ...moreFruits, 'kiwi'];

// Spread in objects
const defaultConfig = { theme: 'dark', language: 'en' };
const userConfig = { language: 'es', notifications: true };
const finalConfig = { ...defaultConfig, ...userConfig };

// Rest parameters
function sum(...numbers) {
  return numbers.reduce((total, num) => total + num, 0);
}

// Classes
class Vehicle {
  constructor(make, model, year) {
    this.make = make;
    this.model = model;
    this.year = year;
  }

  getAge() {
    return new Date().getFullYear() - this.year;
  }

  getInfo() {
    return `${this.year} ${this.make} ${this.model}`;
  }
}

class Car extends Vehicle {
  constructor(make, model, year, doors) {
    super(make, model, year);
    this.doors = doors;
  }

  getType() {
    return this.doors === 2 ? 'Coupe' : 'Sedan';
  }
}

// Modules
// math.js
export const PI = 3.14159;
export function add(a, b) {
  return a + b;
}
export function multiply(a, b) {
  return a * b;
}
export default function calculator() {
  return {
    add,
    multiply,
    PI
  };
}

// main.js
import calculator, { add, PI } from './math.js';
import * as math from './math.js';

const result = add(5, 3);
const area = PI * 5 * 5;
```

### Modern ES Features (ES2017+)
```javascript
// Async/Await (ES2017)
async function fetchUserData(userId) {
  try {
    const response = await fetch(`/api/users/${userId}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const userData = await response.json();
    return userData;
  } catch (error) {
    console.error('Failed to fetch user data:', error);
    throw error;
  }
}

// Parallel async operations
async function fetchMultipleUsers(userIds) {
  const promises = userIds.map(id => fetchUserData(id));
  const users = await Promise.all(promises);
  return users;
}

// Sequential vs Parallel
async function sequentialOperations() {
  const user1 = await fetchUserData(1);  // Wait for this
  const user2 = await fetchUserData(2);  // Then wait for this
  return [user1, user2];
}

async function parallelOperations() {
  const [user1, user2] = await Promise.all([
    fetchUserData(1),  // Start both at the same time
    fetchUserData(2)
  ]);
  return [user1, user2];
}

// Object Rest/Spread (ES2018)
const user = { 
  id: 1, 
  name: 'Alice', 
  email: 'alice@example.com', 
  password: 'secret',
  role: 'admin'
};

const { password, ...publicUser } = user;
const updatedUser = { 
  ...publicUser, 
  lastLogin: new Date(),
  status: 'active'
};

// Optional Chaining (ES2020)
const nestedObject = {
  user: {
    profile: {
      address: {
        street: '123 Main St'
      }
    }
  }
};

// Old way
const street = nestedObject.user && 
              nestedObject.user.profile && 
              nestedObject.user.profile.address && 
              nestedObject.user.profile.address.street;

// Modern way
const modernStreet = nestedObject.user?.profile?.address?.street;

// Nullish Coalescing (ES2020)
const config = {
  theme: null,
  debug: false,
  timeout: 0
};

// Old way (problematic with falsy values)
const theme = config.theme || 'default';  // 'default'
const debug = config.debug || true;       // true (wrong!)
const timeout = config.timeout || 5000;  // 5000 (wrong!)

// Modern way (only null/undefined trigger default)
const modernTheme = config.theme ?? 'default';  // 'default'
const modernDebug = config.debug ?? true;       // false (correct!)
const modernTimeout = config.timeout ?? 5000;  // 0 (correct!)

// BigInt (ES2020)
const largeNumber = 9007199254740991n;
const anotherLarge = BigInt('9007199254740992');
const calculation = largeNumber + anotherLarge;

// Dynamic Imports (ES2020)
async function loadModule(moduleName) {
  const module = await import(`./modules/${moduleName}.js`);
  return module.default;
}

// Conditional module loading
if (process.env.NODE_ENV === 'development') {
  const devTools = await import('./dev-tools.js');
  devTools.initialize();
}

// Private Class Fields (ES2022)
class Counter {
  #count = 0;  // Private field
  #maxCount;   // Private field

  constructor(maxCount = 100) {
    this.#maxCount = maxCount;
  }

  increment() {
    if (this.#count < this.#maxCount) {
      this.#count++;
    }
  }

  get value() {
    return this.#count;
  }

  #validateCount() {  // Private method
    return this.#count >= 0 && this.#count <= this.#maxCount;
  }
}

// Top-level await (ES2022)
// In a module file
const config = await fetch('/api/config').then(r => r.json());
const database = await connectToDatabase(config.db);

export { database };
```

## Node.js and Server-Side JavaScript {#nodejs}

### Node.js Fundamentals
```javascript
// Built-in modules
const fs = require('fs').promises;
const path = require('path');
const http = require('http');
const util = require('util');

// File system operations
async function fileOperations() {
  try {
    // Read file
    const data = await fs.readFile('config.json', 'utf8');
    const config = JSON.parse(data);

    // Write file
    const newConfig = { ...config, lastUpdated: new Date() };
    await fs.writeFile('config.json', JSON.stringify(newConfig, null, 2));

    // Directory operations
    const files = await fs.readdir('./uploads');
    for (const file of files) {
      const stats = await fs.stat(path.join('./uploads', file));
      console.log(`${file}: ${stats.size} bytes`);
    }
  } catch (error) {
    console.error('File operation failed:', error);
  }
}

// HTTP Server
const server = http.createServer(async (req, res) => {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }

  // Route handling
  const url = new URL(req.url, `http://${req.headers.host}`);
  
  if (url.pathname === '/api/users' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ users: [] }));
  } else if (url.pathname === '/api/users' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        const userData = JSON.parse(body);
        // Process user data
        res.writeHead(201, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ id: Date.now(), ...userData }));
      } catch (error) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Invalid JSON' }));
      }
    });
  } else {
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Not found' }));
  }
});

server.listen(3000, () => {
  console.log('Server running on http://localhost:3000');
});

// Express.js Framework
const express = require('express');
const app = express();

// Middleware
app.use(express.json());
app.use(express.static('public'));

// Logging middleware
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
  next();
});

// Authentication middleware
function authenticate(req, res, next) {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }
  
  // Verify token (simplified)
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    res.status(401).json({ error: 'Invalid token' });
  }
}

// Routes
app.get('/api/users', authenticate, async (req, res) => {
  try {
    const users = await getUsersFromDatabase();
    res.json({ users });
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.post('/api/users', async (req, res) => {
  try {
    const { name, email } = req.body;
    
    // Validation
    if (!name || !email) {
      return res.status(400).json({ 
        error: 'Name and email are required' 
      });
    }

    const user = await createUser({ name, email });
    res.status(201).json({ user });
  } catch (error) {
    res.status(500).json({ error: 'Failed to create user' });
  }
});

// Error handling middleware
app.use((error, req, res, next) => {
  console.error(error.stack);
  res.status(500).json({ error: 'Something went wrong!' });
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully');
  server.close(() => {
    console.log('Process terminated');
  });
});
```

### Streams and Performance
```javascript
const fs = require('fs');
const { pipeline, Transform } = require('stream');
const { promisify } = require('util');

const pipelineAsync = promisify(pipeline);

// Transform stream for processing large files
class JSONProcessor extends Transform {
  constructor() {
    super({ objectMode: true });
    this.buffer = '';
  }

  _transform(chunk, encoding, callback) {
    this.buffer += chunk.toString();
    const lines = this.buffer.split('\n');
    this.buffer = lines.pop() || '';

    for (const line of lines) {
      if (line.trim()) {
        try {
          const data = JSON.parse(line);
          // Process data
          const processed = {
            ...data,
            processed: true,
            timestamp: new Date().toISOString()
          };
          this.push(JSON.stringify(processed) + '\n');
        } catch (error) {
          console.error('Invalid JSON:', line);
        }
      }
    }
    callback();
  }

  _flush(callback) {
    if (this.buffer.trim()) {
      try {
        const data = JSON.parse(this.buffer);
        const processed = {
          ...data,
          processed: true,
          timestamp: new Date().toISOString()
        };
        this.push(JSON.stringify(processed) + '\n');
      } catch (error) {
        console.error('Invalid JSON in buffer:', this.buffer);
      }
    }
    callback();
  }
}

// Process large files efficiently
async function processLargeFile(inputPath, outputPath) {
  try {
    await pipelineAsync(
      fs.createReadStream(inputPath),
      new JSONProcessor(),
      fs.createWriteStream(outputPath)
    );
    console.log('File processing completed');
  } catch (error) {
    console.error('Pipeline failed:', error);
  }
}

// Memory-efficient CSV processing
const csv = require('csv-parser');
const csvWriter = require('csv-writer');

async function processCsvFile(inputPath, outputPath) {
  const writer = csvWriter.createObjectCsvWriter({
    path: outputPath,
    header: [
      { id: 'id', title: 'ID' },
      { id: 'name', title: 'Name' },
      { id: 'email', title: 'Email' },
      { id: 'processed', title: 'Processed' }
    ]
  });

  const processedRecords = [];
  
  return new Promise((resolve, reject) => {
    fs.createReadStream(inputPath)
      .pipe(csv())
      .on('data', (data) => {
        // Process each row
        const processed = {
          ...data,
          processed: new Date().toISOString()
        };
        processedRecords.push(processed);

        // Write in batches to avoid memory issues
        if (processedRecords.length >= 1000) {
          writer.writeRecords(processedRecords);
          processedRecords.length = 0;
        }
      })
      .on('end', () => {
        if (processedRecords.length > 0) {
          writer.writeRecords(processedRecords);
        }
        resolve();
      })
      .on('error', reject);
  });
}
```

## Package Management {#package-management}

### npm and package.json
```json
{
  "name": "modern-js-app",
  "version": "1.0.0",
  "description": "A modern JavaScript application",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js",
    "build": "webpack --mode production",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "lint": "eslint src/",
    "lint:fix": "eslint src/ --fix",
    "format": "prettier --write src/",
    "type-check": "tsc --noEmit",
    "prebuild": "npm run lint && npm run test",
    "postinstall": "husky install"
  },
  "dependencies": {
    "express": "^4.18.2",
    "mongoose": "^7.0.0",
    "jsonwebtoken": "^9.0.0",
    "bcryptjs": "^2.4.3",
    "cors": "^2.8.5",
    "helmet": "^6.0.1",
    "dotenv": "^16.0.3"
  },
  "devDependencies": {
    "nodemon": "^2.0.20",
    "jest": "^29.4.0",
    "supertest": "^6.3.3",
    "eslint": "^8.34.0",
    "prettier": "^2.8.4",
    "husky": "^8.0.3",
    "lint-staged": "^13.1.2",
    "@types/node": "^18.14.0",
    "typescript": "^4.9.5"
  },
  "engines": {
    "node": ">=16.0.0",
    "npm": ">=8.0.0"
  },
  "lint-staged": {
    "*.{js,ts}": [
      "eslint --fix",
      "prettier --write"
    ]
  },
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged",
      "pre-push": "npm test"
    }
  }
}
```

### Yarn and Advanced Features
```bash
# Yarn workspace configuration
# package.json (root)
{
  "private": true,
  "workspaces": [
    "packages/*",
    "apps/*"
  ],
  "scripts": {
    "build": "yarn workspaces run build",
    "test": "yarn workspaces run test",
    "dev": "concurrently \"yarn workspace @myapp/api dev\" \"yarn workspace @myapp/web dev\""
  }
}

# packages/shared/package.json
{
  "name": "@myapp/shared",
  "version": "1.0.0",
  "main": "dist/index.js",
  "dependencies": {
    "lodash": "^4.17.21"
  }
}

# apps/api/package.json
{
  "name": "@myapp/api",
  "version": "1.0.0",
  "dependencies": {
    "@myapp/shared": "1.0.0",
    "express": "^4.18.2"
  }
}

# Yarn commands
yarn install                    # Install dependencies
yarn add express               # Add dependency
yarn add -D jest              # Add dev dependency
yarn workspace @myapp/api add mongoose  # Add to specific workspace
yarn workspaces run build     # Run script in all workspaces
yarn workspace @myapp/api test  # Run script in specific workspace
```

### pnpm - Efficient Package Manager
```bash
# pnpm features
pnpm install                   # Fast, disk-efficient installs
pnpm add express              # Add dependency
pnpm run build                # Run scripts
pnpm exec eslint .            # Execute package binaries

# pnpm workspace (pnpm-workspace.yaml)
packages:
  - 'packages/*'
  - 'apps/*'
  - '!**/test/**'

# Efficient storage and linking
# Creates hard links instead of duplicating files
# Saves significant disk space in monorepos
```

### Package Security and Auditing
```bash
# Security auditing
npm audit                      # Check for vulnerabilities
npm audit fix                 # Automatically fix issues
npm audit fix --force         # Force fixes (may break things)

# Yarn security
yarn audit                    # Check vulnerabilities
yarn audit --json            # JSON output for CI/CD

# Alternative tools
npx audit-ci                  # Audit in CI/CD pipelines
npx snyk test                 # Comprehensive security testing
npx depcheck                  # Find unused dependencies
npx npm-check-updates         # Check for package updates
```

## Build Tools and Bundlers {#build-tools}

### Webpack Configuration
```javascript
// webpack.config.js
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const TerserPlugin = require('terser-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

module.exports = (env, argv) => {
  const isProduction = argv.mode === 'production';
  
  return {
    entry: {
      main: './src/index.js',
      vendor: ['react', 'react-dom', 'lodash']
    },
    
    output: {
      path: path.resolve(__dirname, 'dist'),
      filename: isProduction 
        ? '[name].[contenthash].js' 
        : '[name].js',
      publicPath: '/',
      clean: true
    },

    module: {
      rules: [
        {
          test: /\.(js|jsx)$/,
          exclude: /node_modules/,
          use: {
            loader: 'babel-loader',
            options: {
              presets: [
                ['@babel/preset-env', { targets: 'defaults' }],
                '@babel/preset-react'
              ],
              plugins: [
                '@babel/plugin-proposal-class-properties',
                isProduction && 'transform-remove-console'
              ].filter(Boolean)
            }
          }
        },
        {
          test: /\.css$/,
          use: [
            isProduction ? MiniCssExtractPlugin.loader : 'style-loader',
            'css-loader',
            'postcss-loader'
          ]
        },
        {
          test: /\.scss$/,
          use: [
            isProduction ? MiniCssExtractPlugin.loader : 'style-loader',
            'css-loader',
            'postcss-loader',
            'sass-loader'
          ]
        },
        {
          test: /\.(png|jpe?g|gif|svg)$/,
          type: 'asset/resource',
          generator: {
            filename: 'images/[name].[contenthash][ext]'
          }
        },
        {
          test: /\.(woff|woff2|eot|ttf|otf)$/,
          type: 'asset/resource',
          generator: {
            filename: 'fonts/[name].[contenthash][ext]'
          }
        }
      ]
    },

    plugins: [
      new CleanWebpackPlugin(),
      new HtmlWebpackPlugin({
        template: './public/index.html',
        minify: isProduction ? {
          removeComments: true,
          collapseWhitespace: true,
          removeRedundantAttributes: true,
          useShortDoctype: true,
          removeEmptyAttributes: true,
          removeStyleLinkTypeAttributes: true,
          keepClosingSlash: true,
          minifyJS: true,
          minifyCSS: true,
          minifyURLs: true
        } : false
      }),
      isProduction && new MiniCssExtractPlugin({
        filename: '[name].[contenthash].css',
        chunkFilename: '[id].[contenthash].css'
      })
    ].filter(Boolean),

    optimization: {
      minimize: isProduction,
      minimizer: [
        new TerserPlugin({
          terserOptions: {
            compress: {
              drop_console: true,
              drop_debugger: true
            }
          }
        })
      ],
      splitChunks: {
        chunks: 'all',
        cacheGroups: {
          vendor: {
            test: /[\\/]node_modules[\\/]/,
            name: 'vendors',
            chunks: 'all'
          }
        }
      }
    },

    devServer: {
      contentBase: path.join(__dirname, 'dist'),
      compress: true,
      port: 3000,
      hot: true,
      historyApiFallback: true,
      open: true
    },

    devtool: isProduction ? 'source-map' : 'eval-source-map',

    resolve: {
      extensions: ['.js', '.jsx', '.ts', '.tsx'],
      alias: {
        '@': path.resolve(__dirname, 'src'),
        '@components': path.resolve(__dirname, 'src/components'),
        '@utils': path.resolve(__dirname, 'src/utils')
      }
    }
  };
};
```

### Vite - Next Generation Build Tool
```javascript
// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig({
  plugins: [react()],
  
  build: {
    outDir: 'dist',
    sourcemap: true,
    minify: 'terser',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          utils: ['lodash', 'date-fns']
        }
      }
    }
  },

  server: {
    port: 3000,
    open: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  },

  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
      '@components': resolve(__dirname, 'src/components')
    }
  },

  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@import "@/styles/variables.scss";`
      }
    }
  }
});

// Lightning fast HMR and build times
// Native ES modules support
// Built-in TypeScript support
// Optimized for modern browsers
```

### Rollup for Library Building
```javascript
// rollup.config.js
import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import babel from '@rollup/plugin-babel';
import terser from '@rollup/plugin-terser';
import { fileURLToPath } from 'url';

const __dirname = fileURLToPath(new URL('.', import.meta.url));

export default {
  input: 'src/index.js',
  
  output: [
    {
      file: 'dist/my-library.js',
      format: 'umd',
      name: 'MyLibrary',
      globals: {
        react: 'React',
        'react-dom': 'ReactDOM'
      }
    },
    {
      file: 'dist/my-library.esm.js',
      format: 'esm'
    },
    {
      file: 'dist/my-library.cjs.js',
      format: 'cjs'
    }
  ],

  external: ['react', 'react-dom'],

  plugins: [
    resolve({
      browser: true,
      preferBuiltins: false
    }),
    commonjs(),
    babel({
      babelHelpers: 'bundled',
      exclude: 'node_modules/**',
      presets: [
        ['@babel/preset-env', { modules: false }],
        '@babel/preset-react'
      ]
    }),
    terser()
  ]
};
```

## Testing Frameworks {#testing}

### Jest Testing Framework
```javascript
// jest.config.js
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.js'],
  testMatch: [
    '<rootDir>/src/**/__tests__/**/*.{js,jsx,ts,tsx}',
    '<rootDir>/src/**/*.{test,spec}.{js,jsx,ts,tsx}'
  ],
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/index.js',
    '!src/reportWebVitals.js'
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },
  moduleNameMapping: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy'
  },
  transform: {
    '^.+\\.(js|jsx|ts|tsx)$': 'babel-jest'
  }
};

// Example test file
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import UserForm from '../UserForm';
import { createUser } from '../api/users';

// Mock API calls
jest.mock('../api/users');
const mockCreateUser = createUser as jest.MockedFunction<typeof createUser>;

describe('UserForm', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders form fields correctly', () => {
    render(<UserForm onSubmit={jest.fn()} />);
    
    expect(screen.getByLabelText(/name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /submit/i })).toBeInTheDocument();
  });

  it('validates required fields', async () => {
    const mockOnSubmit = jest.fn();
    render(<UserForm onSubmit={mockOnSubmit} />);
    
    fireEvent.click(screen.getByRole('button', { name: /submit/i }));
    
    await waitFor(() => {
      expect(screen.getByText(/name is required/i)).toBeInTheDocument();
      expect(screen.getByText(/email is required/i)).toBeInTheDocument();
    });
    
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it('submits form with valid data', async () => {
    const mockUser = { id: 1, name: 'John Doe', email: 'john@example.com' };
    mockCreateUser.mockResolvedValueOnce(mockUser);
    
    const mockOnSubmit = jest.fn();
    render(<UserForm onSubmit={mockOnSubmit} />);
    
    fireEvent.change(screen.getByLabelText(/name/i), {
      target: { value: 'John Doe' }
    });
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'john@example.com' }
    });
    
    fireEvent.click(screen.getByRole('button', { name: /submit/i }));
    
    await waitFor(() => {
      expect(mockCreateUser).toHaveBeenCalledWith({
        name: 'John Doe',
        email: 'john@example.com'
      });
      expect(mockOnSubmit).toHaveBeenCalledWith(mockUser);
    });
  });

  it('handles API errors gracefully', async () => {
    mockCreateUser.mockRejectedValueOnce(new Error('API Error'));
    
    render(<UserForm onSubmit={jest.fn()} />);
    
    fireEvent.change(screen.getByLabelText(/name/i), {
      target: { value: 'John Doe' }
    });
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'john@example.com' }
    });
    
    fireEvent.click(screen.getByRole('button', { name: /submit/i }));
    
    await waitFor(() => {
      expect(screen.getByText(/failed to create user/i)).toBeInTheDocument();
    });
  });
});

// Utility functions for testing
export const renderWithProviders = (ui, options = {}) => {
  const { theme = 'light', ...renderOptions } = options;
  
  function Wrapper({ children }) {
    return (
      <ThemeProvider theme={theme}>
        <Router>
          {children}
        </Router>
      </ThemeProvider>
    );
  }
  
  return render(ui, { wrapper: Wrapper, ...renderOptions });
};

// Custom hooks testing
import { renderHook, act } from '@testing-library/react';
import useCounter from '../useCounter';

describe('useCounter', () => {
  it('should initialize with default value', () => {
    const { result } = renderHook(() => useCounter());
    expect(result.current.count).toBe(0);
  });

  it('should increment count', () => {
    const { result } = renderHook(() => useCounter());
    
    act(() => {
      result.current.increment();
    });
    
    expect(result.current.count).toBe(1);
  });
});
```

### Playwright for E2E Testing
```javascript
// playwright.config.js
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure'
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] }
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] }
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] }
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] }
    }
  ],

  webServer: {
    command: 'npm start',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI
  }
});

// Example E2E test
import { test, expect } from '@playwright/test';

test.describe('User Management', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should create a new user', async ({ page }) => {
    // Navigate to user creation form
    await page.click('text=Add User');
    await expect(page).toHaveURL('/users/new');

    // Fill form
    await page.fill('[data-testid=user-name]', 'John Doe');
    await page.fill('[data-testid=user-email]', 'john@example.com');
    
    // Submit form
    await page.click('[data-testid=submit-button]');
    
    // Verify success
    await expect(page.locator('.success-message')).toContainText(
      'User created successfully'
    );
    
    // Verify user appears in list
    await page.goto('/users');
    await expect(page.locator('[data-testid=user-list]')).toContainText('John Doe');
  });

  test('should handle form validation', async ({ page }) => {
    await page.click('text=Add User');
    
    // Try to submit empty form
    await page.click('[data-testid=submit-button]');
    
    // Check validation messages
    await expect(page.locator('.error-message')).toContainText('Name is required');
    await expect(page.locator('.error-message')).toContainText('Email is required');
  });

  test('should be responsive on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    
    // Check mobile navigation
    await page.click('[data-testid=mobile-menu-button]');
    await expect(page.locator('[data-testid=mobile-menu]')).toBeVisible();
    
    // Check form is usable on mobile
    await page.click('text=Add User');
    await page.fill('[data-testid=user-name]', 'Mobile User');
    await page.fill('[data-testid=user-email]', 'mobile@example.com');
    await page.click('[data-testid=submit-button]');
    
    await expect(page.locator('.success-message')).toBeVisible();
  });
});
```

This comprehensive guide covers the modern JavaScript ecosystem from language features to tooling and testing. The JavaScript ecosystem continues to evolve rapidly, with new tools and frameworks emerging regularly. The key is to understand the fundamentals and choose the right tools for your specific project needs.

Remember that while the ecosystem offers many choices, it's important to balance innovation with stability, especially in production applications. Start with well-established tools and gradually adopt newer technologies as they mature and provide clear benefits to your development workflow.''',
            'category': 'JavaScript',
            'tags': 'javascript,ecosystem,nodejs,frameworks',
        },
        {
            'title': 'HTML5 Semantic Architecture',
            'content': '''# HTML5 Semantic Architecture: Building Meaningful Web Structure

## Table of Contents
1. [Introduction to Semantic HTML](#introduction)
2. [HTML5 Semantic Elements](#semantic-elements)
3. [Document Structure and Hierarchy](#document-structure)
4. [Accessibility and ARIA](#accessibility)
5. [SEO Benefits](#seo)
6. [Microdata and Structured Data](#microdata)
7. [Form Semantics](#forms)
8. [Progressive Enhancement](#progressive-enhancement)
9. [Browser Support and Polyfills](#browser-support)
10. [Best Practices](#best-practices)

## Introduction to Semantic HTML {#introduction}

Semantic HTML is the practice of using HTML markup to reinforce the meaning and purpose of content rather than just its appearance. HTML5 introduced many semantic elements that provide clear meaning about the structure and content of web pages.

### Why Semantic HTML Matters
- **Accessibility**: Screen readers and assistive technologies understand content better
- **SEO**: Search engines can better index and understand your content
- **Maintainability**: Code is more readable and easier to maintain
- **Future-proofing**: Semantic markup adapts better to new devices and contexts
- **Performance**: Can enable better optimization by browsers and tools

### Semantic vs Non-Semantic Markup
```html
<!-- Non-semantic approach -->
<div class="header">
  <div class="navigation">
    <div class="nav-item">Home</div>
    <div class="nav-item">About</div>
    <div class="nav-item">Contact</div>
  </div>
</div>

<div class="main-content">
  <div class="article">
    <div class="article-title">Understanding Semantic HTML</div>
    <div class="article-content">
      Content goes here...
    </div>
  </div>
</div>

<div class="sidebar">
  <div class="widget">Related Articles</div>
</div>

<div class="footer">
  <div class="copyright">© 2023 Example Site</div>
</div>

<!-- Semantic approach -->
<header>
  <nav>
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/about">About</a></li>
      <li><a href="/contact">Contact</a></li>
    </ul>
  </nav>
</header>

<main>
  <article>
    <h1>Understanding Semantic HTML</h1>
    <section>
      <p>Content goes here...</p>
    </section>
  </article>
</main>

<aside>
  <section>
    <h2>Related Articles</h2>
    <ul>
      <li><a href="/article1">Article 1</a></li>
      <li><a href="/article2">Article 2</a></li>
    </ul>
  </section>
</aside>

<footer>
  <p>&copy; 2023 Example Site</p>
</footer>
```

## HTML5 Semantic Elements {#semantic-elements}

### Document Structure Elements

#### Header Element
```html
<!-- Site header -->
<header>
  <h1>Company Name</h1>
  <nav>
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/products">Products</a></li>
      <li><a href="/about">About</a></li>
    </ul>
  </nav>
</header>

<!-- Article header -->
<article>
  <header>
    <h2>Article Title</h2>
    <p>By <strong>Author Name</strong></p>
    <time datetime="2023-12-01">December 1, 2023</time>
  </header>
  <p>Article content...</p>
</article>

<!-- Section header -->
<section>
  <header>
    <h3>Section Title</h3>
    <p>Section introduction</p>
  </header>
  <p>Section content...</p>
</section>
```

#### Navigation Element
```html
<!-- Main site navigation -->
<nav role="navigation" aria-label="Main navigation">
  <ul>
    <li><a href="/" aria-current="page">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li><a href="/services">Services</a></li>
    <li><a href="/contact">Contact</a></li>
  </ul>
</nav>

<!-- Breadcrumb navigation -->
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li><a href="/products/laptops">Laptops</a></li>
    <li aria-current="page">Gaming Laptops</li>
  </ol>
</nav>

<!-- Table of contents -->
<nav aria-label="Table of contents">
  <ol>
    <li><a href="#introduction">Introduction</a></li>
    <li><a href="#methods">Methods</a></li>
    <li><a href="#results">Results</a></li>
    <li><a href="#conclusion">Conclusion</a></li>
  </ol>
</nav>

<!-- Pagination -->
<nav aria-label="Pagination">
  <ul>
    <li><a href="/page/1" aria-label="Go to first page">1</a></li>
    <li><a href="/page/2">2</a></li>
    <li><span aria-current="page" aria-label="Current page">3</span></li>
    <li><a href="/page/4">4</a></li>
    <li><a href="/page/5" aria-label="Go to last page">5</a></li>
  </ul>
</nav>
```

#### Main Content Element
```html
<!-- The main content area -->
<main id="main-content">
  <h1>Welcome to Our Website</h1>
  <p>This is the primary content of the page.</p>
  
  <section id="featured-products">
    <h2>Featured Products</h2>
    <!-- Product listings -->
  </section>
  
  <section id="testimonials">
    <h2>Customer Testimonials</h2>
    <!-- Testimonials -->
  </section>
</main>

<!-- Skip to main content link for accessibility -->
<a href="#main-content" class="skip-link">Skip to main content</a>
```

#### Article Element
```html
<!-- Blog post -->
<article>
  <header>
    <h1>The Future of Web Development</h1>
    <p>Published by <a href="/authors/jane-doe">Jane Doe</a></p>
    <time datetime="2023-12-01T10:30:00Z">December 1, 2023</time>
    <div class="tags">
      <span class="tag">Web Development</span>
      <span class="tag">HTML5</span>
      <span class="tag">Semantic Web</span>
    </div>
  </header>
  
  <section>
    <h2>Introduction</h2>
    <p>Web development continues to evolve...</p>
  </section>
  
  <section>
    <h2>Current Trends</h2>
    <p>Several trends are shaping the industry...</p>
  </section>
  
  <footer>
    <div class="article-meta">
      <div class="share-buttons">
        <button type="button" onclick="share('twitter')">Share on Twitter</button>
        <button type="button" onclick="share('facebook')">Share on Facebook</button>
      </div>
      <div class="article-stats">
        <span>1,234 views</span>
        <span>56 comments</span>
      </div>
    </div>
  </footer>
</article>

<!-- Product review -->
<article itemscope itemtype="http://schema.org/Review">
  <header>
    <h3 itemprop="name">Amazing Laptop Review</h3>
    <div itemprop="reviewRating" itemscope itemtype="http://schema.org/Rating">
      <span itemprop="ratingValue">5</span> out of 
      <span itemprop="bestRating">5</span> stars
    </div>
  </header>
  
  <div itemprop="reviewBody">
    <p>This laptop exceeded my expectations in every way...</p>
  </div>
  
  <footer>
    <p>Reviewed by <span itemprop="author">John Smith</span> on 
       <time itemprop="datePublished" datetime="2023-11-15">November 15, 2023</time>
    </p>
  </footer>
</article>
```

#### Section Element
```html
<!-- Document sections -->
<main>
  <section id="about-us">
    <h2>About Our Company</h2>
    <p>We are a leading provider of...</p>
    
    <section id="our-history">
      <h3>Our History</h3>
      <p>Founded in 1995...</p>
    </section>
    
    <section id="our-mission">
      <h3>Our Mission</h3>
      <p>To provide exceptional service...</p>
    </section>
  </section>
  
  <section id="services">
    <h2>Our Services</h2>
    <div class="service-grid">
      <article class="service">
        <h3>Web Development</h3>
        <p>Custom web applications...</p>
      </article>
      <article class="service">
        <h3>Mobile Apps</h3>
        <p>Native and hybrid mobile solutions...</p>
      </article>
    </div>
  </section>
</main>
```

#### Aside Element
```html
<!-- Sidebar content -->
<aside>
  <section>
    <h3>Related Articles</h3>
    <ul>
      <li><a href="/html-best-practices">HTML Best Practices</a></li>
      <li><a href="/css-architecture">CSS Architecture</a></li>
      <li><a href="/javascript-patterns">JavaScript Patterns</a></li>
    </ul>
  </section>
  
  <section>
    <h3>Advertisement</h3>
    <div class="ad-container">
      <!-- Ad content -->
    </div>
  </section>
</aside>

<!-- Pull quote in article -->
<article>
  <p>The importance of semantic HTML cannot be overstated...</p>
  
  <aside>
    <blockquote>
      "Semantic HTML is the foundation of accessible web design"
      <cite>- Web Accessibility Expert</cite>
    </blockquote>
  </aside>
  
  <p>This approach ensures that content is meaningful...</p>
</article>
```

#### Footer Element
```html
<!-- Site footer -->
<footer>
  <div class="footer-content">
    <section>
      <h3>Contact Information</h3>
      <address>
        <p>123 Web Street<br>
           Internet City, IC 12345</p>
        <p>Phone: <a href="tel:+1234567890">(123) 456-7890</a></p>
        <p>Email: <a href="mailto:info@example.com">info@example.com</a></p>
      </address>
    </section>
    
    <section>
      <h3>Quick Links</h3>
      <nav>
        <ul>
          <li><a href="/privacy">Privacy Policy</a></li>
          <li><a href="/terms">Terms of Service</a></li>
          <li><a href="/sitemap">Sitemap</a></li>
        </ul>
      </nav>
    </section>
    
    <section>
      <h3>Follow Us</h3>
      <ul class="social-links">
        <li><a href="https://twitter.com/example" aria-label="Follow us on Twitter">Twitter</a></li>
        <li><a href="https://facebook.com/example" aria-label="Follow us on Facebook">Facebook</a></li>
        <li><a href="https://linkedin.com/company/example" aria-label="Follow us on LinkedIn">LinkedIn</a></li>
      </ul>
    </section>
  </div>
  
  <div class="footer-bottom">
    <p>&copy; 2023 Example Company. All rights reserved.</p>
  </div>
</footer>

<!-- Article footer -->
<article>
  <h2>Article Title</h2>
  <p>Article content...</p>
  
  <footer>
    <div class="article-meta">
      <p>Last updated: <time datetime="2023-12-01">December 1, 2023</time></p>
      <div class="author-info">
        <img src="/authors/jane-doe.jpg" alt="Jane Doe" width="50" height="50">
        <div>
          <p><strong>Jane Doe</strong></p>
          <p>Senior Web Developer</p>
        </div>
      </div>
    </div>
  </footer>
</article>
```

### Content Sectioning Elements

#### Figure and Figcaption
```html
<!-- Image with caption -->
<figure>
  <img src="/charts/revenue-2023.png" 
       alt="Bar chart showing revenue growth from Q1 to Q4 2023"
       width="600" 
       height="400">
  <figcaption>
    Revenue growth throughout 2023, showing a 150% increase from Q1 to Q4
  </figcaption>
</figure>

<!-- Code example with caption -->
<figure>
  <pre><code class="language-javascript">
function calculateArea(radius) {
  return Math.PI * radius * radius;
}
  </code></pre>
  <figcaption>
    Example function to calculate the area of a circle
  </figcaption>
</figure>

<!-- Quote with citation -->
<figure>
  <blockquote>
    <p>The best way to predict the future is to invent it.</p>
  </blockquote>
  <figcaption>
    <cite>Alan Kay</cite>, computer scientist
  </figcaption>
</figure>

<!-- Video with description -->
<figure>
  <video controls width="600" height="400">
    <source src="/videos/tutorial.mp4" type="video/mp4">
    <source src="/videos/tutorial.webm" type="video/webm">
    <track kind="captions" src="/captions/tutorial-en.vtt" srclang="en" label="English">
    Your browser does not support the video tag.
  </video>
  <figcaption>
    Tutorial: Getting Started with HTML5 Semantic Elements
  </figcaption>
</figure>
```

#### Details and Summary
```html
<!-- FAQ section -->
<section id="faq">
  <h2>Frequently Asked Questions</h2>
  
  <details>
    <summary>What is semantic HTML?</summary>
    <p>Semantic HTML is the use of HTML markup to reinforce the semantics, 
       or meaning, of the information in webpages rather than merely to 
       define its presentation or look.</p>
  </details>
  
  <details>
    <summary>Why is accessibility important?</summary>
    <p>Accessibility ensures that websites and applications can be used 
       by people with disabilities, providing equal access to information 
       and functionality.</p>
  </details>
  
  <details open>
    <summary>How do I test for accessibility?</summary>
    <div>
      <p>There are several ways to test for accessibility:</p>
      <ul>
        <li>Use automated testing tools like axe or Lighthouse</li>
        <li>Test with screen readers</li>
        <li>Navigate using only the keyboard</li>
        <li>Check color contrast ratios</li>
      </ul>
    </div>
  </details>
</section>

<!-- Settings panel -->
<details class="settings-panel">
  <summary>Advanced Settings</summary>
  <form>
    <fieldset>
      <legend>Notification Preferences</legend>
      <label>
        <input type="checkbox" name="email" checked>
        Email notifications
      </label>
      <label>
        <input type="checkbox" name="sms">
        SMS notifications
      </label>
    </fieldset>
  </form>
</details>
```

## Document Structure and Hierarchy {#document-structure}

### Proper Heading Hierarchy
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Semantic HTML Guide - Web Development Blog</title>
</head>
<body>
  <header>
    <h1>Web Development Blog</h1> <!-- Site title -->
    <nav>
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/tutorials">Tutorials</a></li>
        <li><a href="/about">About</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <article>
      <header>
        <h1>Understanding Semantic HTML</h1> <!-- Page/Article title -->
        <p>A comprehensive guide to writing meaningful markup</p>
      </header>

      <section>
        <h2>Introduction</h2> <!-- Major section -->
        <p>HTML5 introduced many semantic elements...</p>

        <section>
          <h3>What is Semantic HTML?</h3> <!-- Subsection -->
          <p>Semantic HTML refers to...</p>

          <section>
            <h4>Benefits of Semantic Markup</h4> <!-- Sub-subsection -->
            <ul>
              <li>Improved accessibility</li>
              <li>Better SEO</li>
              <li>Easier maintenance</li>
            </ul>
          </section>
        </section>
      </section>

      <section>
        <h2>HTML5 Semantic Elements</h2>
        
        <section>
          <h3>Structural Elements</h3>
          
          <section>
            <h4>Header Element</h4>
            <p>The header element represents...</p>
          </section>
          
          <section>
            <h4>Nav Element</h4>
            <p>The nav element represents...</p>
          </section>
        </section>
      </section>
    </article>
  </main>

  <aside>
    <section>
      <h2>Related Articles</h2> <!-- Sidebar heading -->
      <ul>
        <li><a href="/css-grid">CSS Grid Layout</a></li>
        <li><a href="/responsive-design">Responsive Design</a></li>
      </ul>
    </section>
  </aside>

  <footer>
    <p>&copy; 2023 Web Development Blog</p>
  </footer>
</body>
</html>
```

### Landmark Roles
```html
<!-- Explicit ARIA landmarks -->
<body>
  <header role="banner">
    <h1>Site Title</h1>
    <nav role="navigation" aria-label="Main navigation">
      <!-- Navigation content -->
    </nav>
  </header>

  <main role="main">
    <article role="article">
      <!-- Article content -->
    </article>
  </main>

  <aside role="complementary">
    <!-- Sidebar content -->
  </aside>

  <footer role="contentinfo">
    <!-- Footer content -->
  </footer>
</body>

<!-- Implicit landmarks (HTML5 semantic elements automatically provide roles) -->
<body>
  <header> <!-- Automatically has banner role -->
    <nav> <!-- Automatically has navigation role -->
    </nav>
  </header>
  
  <main> <!-- Automatically has main role -->
  </main>
  
  <aside> <!-- Automatically has complementary role -->
  </aside>
  
  <footer> <!-- Automatically has contentinfo role -->
  </footer>
</body>
```

## Accessibility and ARIA {#accessibility}

### ARIA Attributes for Enhanced Semantics
```html
<!-- Form with ARIA labels -->
<form role="search" aria-label="Site search">
  <div class="form-group">
    <label for="search-input">Search</label>
    <input type="search" 
           id="search-input" 
           name="query"
           aria-describedby="search-help"
           aria-required="true"
           placeholder="Enter search terms">
    <div id="search-help" class="help-text">
      Search across all articles and tutorials
    </div>
  </div>
  <button type="submit" aria-label="Submit search">
    <span aria-hidden="true">🔍</span>
    Search
  </button>
</form>

<!-- Navigation with current page indication -->
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/" aria-current="page">Home</a></li>
    <li><a href="/about">About</a></li>
    <li><a href="/contact">Contact</a></li>
  </ul>
</nav>

<!-- Dynamic content updates -->
<div id="status-message" 
     role="status" 
     aria-live="polite" 
     aria-atomic="true">
  <!-- Status messages will be announced by screen readers -->
</div>

<div id="error-message" 
     role="alert" 
     aria-live="assertive">
  <!-- Error messages will interrupt screen reader -->
</div>

<!-- Expandable content -->
<button type="button" 
        aria-expanded="false" 
        aria-controls="menu-content"
        aria-label="Open main menu">
  Menu
</button>
<div id="menu-content" aria-hidden="true">
  <!-- Menu items -->
</div>

<!-- Data tables -->
<table role="table" aria-label="Sales data for Q4 2023">
  <caption>Quarterly sales figures by region</caption>
  <thead>
    <tr>
      <th scope="col" id="region">Region</th>
      <th scope="col" id="q1">Q1 Sales</th>
      <th scope="col" id="q2">Q2 Sales</th>
      <th scope="col" id="q3">Q3 Sales</th>
      <th scope="col" id="q4">Q4 Sales</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row" id="north">North America</th>
      <td headers="north q1">$1.2M</td>
      <td headers="north q2">$1.5M</td>
      <td headers="north q3">$1.8M</td>
      <td headers="north q4">$2.1M</td>
    </tr>
    <tr>
      <th scope="row" id="europe">Europe</th>
      <td headers="europe q1">$800K</td>
      <td headers="europe q2">$950K</td>
      <td headers="europe q3">$1.1M</td>
      <td headers="europe q4">$1.3M</td>
    </tr>
  </tbody>
</table>
```

### Skip Links and Focus Management
```html
<!-- Skip links for keyboard navigation -->
<body>
  <a href="#main-content" class="skip-link">Skip to main content</a>
  <a href="#main-navigation" class="skip-link">Skip to navigation</a>
  
  <header>
    <nav id="main-navigation" aria-label="Main navigation">
      <!-- Navigation -->
    </nav>
  </header>
  
  <main id="main-content">
    <!-- Main content -->
  </main>
</body>

<style>
.skip-link {
  position: absolute;
  top: -40px;
  left: 6px;
  background: #000;
  color: white;
  padding: 8px;
  text-decoration: none;
  z-index: 1000;
}

.skip-link:focus {
  top: 6px;
}
</style>

<!-- Focus management in single-page applications -->
<script>
function navigateToPage(pageTitle, contentHtml) {
  // Update page content
  document.getElementById('main-content').innerHTML = contentHtml;
  
  // Update page title
  document.title = pageTitle;
  
  // Set focus to main content for screen readers
  const mainContent = document.getElementById('main-content');
  mainContent.setAttribute('tabindex', '-1');
  mainContent.focus();
  
  // Announce page change to screen readers
  const announcement = document.getElementById('page-announcement');
  announcement.textContent = `Navigated to ${pageTitle}`;
}
</script>

<div id="page-announcement" 
     role="status" 
     aria-live="polite" 
     class="sr-only">
</div>
```

## SEO Benefits {#seo}

### Structured Content for Search Engines
```html
<!-- Article with rich semantic markup -->
<article itemscope itemtype="http://schema.org/Article">
  <header>
    <h1 itemprop="headline">
      The Complete Guide to HTML5 Semantic Elements
    </h1>
    
    <div class="article-meta">
      <address itemprop="author" itemscope itemtype="http://schema.org/Person">
        By <span itemprop="name">Jane Developer</span>
      </address>
      
      <time itemprop="datePublished" datetime="2023-12-01T10:00:00Z">
        December 1, 2023
      </time>
      
      <time itemprop="dateModified" datetime="2023-12-01T15:30:00Z">
        Updated: December 1, 2023
      </time>
    </div>
    
    <div itemprop="description">
      Learn how to use HTML5 semantic elements to create more accessible, 
      SEO-friendly, and maintainable web pages.
    </div>
  </header>
  
  <div itemprop="articleBody">
    <section>
      <h2>Introduction</h2>
      <p>HTML5 introduced a set of semantic elements that provide meaning...</p>
    </section>
    
    <section>
      <h2>Key Benefits</h2>
      <ul>
        <li>Improved accessibility for users with disabilities</li>
        <li>Better search engine optimization</li>
        <li>Cleaner, more maintainable code</li>
      </ul>
    </section>
  </div>
  
  <footer>
    <div itemprop="publisher" itemscope itemtype="http://schema.org/Organization">
      <span itemprop="name">Web Development Blog</span>
    </div>
  </footer>
</article>

<!-- Breadcrumb navigation -->
<nav aria-label="Breadcrumb" itemscope itemtype="http://schema.org/BreadcrumbList">
  <ol>
    <li itemprop="itemListElement" itemscope itemtype="http://schema.org/ListItem">
      <a itemprop="item" href="/">
        <span itemprop="name">Home</span>
      </a>
      <meta itemprop="position" content="1">
    </li>
    <li itemprop="itemListElement" itemscope itemtype="http://schema.org/ListItem">
      <a itemprop="item" href="/tutorials">
        <span itemprop="name">Tutorials</span>
      </a>
      <meta itemprop="position" content="2">
    </li>
    <li itemprop="itemListElement" itemscope itemtype="http://schema.org/ListItem">
      <span itemprop="name">HTML5 Semantic Elements</span>
      <meta itemprop="position" content="3">
    </li>
  </ol>
</nav>
```

### Meta Tags and Open Graph
```html
<head>
  <!-- Basic meta tags -->
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>HTML5 Semantic Architecture Guide - Web Dev Blog</title>
  <meta name="description" content="Learn to build meaningful web structure with HTML5 semantic elements. Improve accessibility, SEO, and code maintainability.">
  <meta name="keywords" content="HTML5, semantic elements, web accessibility, SEO, web development">
  <meta name="author" content="Jane Developer">
  
  <!-- Open Graph meta tags for social sharing -->
  <meta property="og:title" content="HTML5 Semantic Architecture Guide">
  <meta property="og:description" content="Master HTML5 semantic elements for better accessibility and SEO">
  <meta property="og:image" content="/images/html5-semantic-guide.jpg">
  <meta property="og:url" content="https://example.com/html5-semantic-guide">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Web Development Blog">
  
  <!-- Twitter Card meta tags -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="HTML5 Semantic Architecture Guide">
  <meta name="twitter:description" content="Master HTML5 semantic elements for better accessibility and SEO">
  <meta name="twitter:image" content="/images/html5-semantic-guide.jpg">
  <meta name="twitter:creator" content="@janedev">
  
  <!-- Canonical URL -->
  <link rel="canonical" href="https://example.com/html5-semantic-guide">
  
  <!-- Structured data -->
  <script type="application/ld+json">
  {
    "@context": "http://schema.org",
    "@type": "Article",
    "headline": "HTML5 Semantic Architecture Guide",
    "description": "Learn to build meaningful web structure with HTML5 semantic elements",
    "author": {
      "@type": "Person",
      "name": "Jane Developer"
    },
    "publisher": {
      "@type": "Organization",
      "name": "Web Development Blog",
      "logo": {
        "@type": "ImageObject",
        "url": "https://example.com/logo.png"
      }
    },
    "datePublished": "2023-12-01T10:00:00Z",
    "dateModified": "2023-12-01T15:30:00Z",
    "image": "https://example.com/images/html5-semantic-guide.jpg",
    "url": "https://example.com/html5-semantic-guide"
  }
  </script>
</head>
```

## Microdata and Structured Data {#microdata}

### Schema.org Markup Examples
```html
<!-- Organization information -->
<div itemscope itemtype="http://schema.org/Organization">
  <h1 itemprop="name">ACME Web Development</h1>
  
  <div itemprop="address" itemscope itemtype="http://schema.org/PostalAddress">
    <span itemprop="streetAddress">123 Web Street</span>,
    <span itemprop="addressLocality">Tech City</span>,
    <span itemprop="addressRegion">CA</span>
    <span itemprop="postalCode">90210</span>
  </div>
  
  <div>Phone: <span itemprop="telephone">+1-555-123-4567</span></div>
  <div>Email: <a href="mailto:info@acme.com" itemprop="email">info@acme.com</a></div>
  <div>Website: <a href="https://acme.com" itemprop="url">acme.com</a></div>
</div>

<!-- Product information -->
<div itemscope itemtype="http://schema.org/Product">
  <h2 itemprop="name">Professional Website Package</h2>
  
  <div itemprop="description">
    Complete website development package including design, development, 
    and hosting setup.
  </div>
  
  <div itemprop="offers" itemscope itemtype="http://schema.org/Offer">
    <span itemprop="price">2999.00</span>
    <span itemprop="priceCurrency">USD</span>
    <span itemprop="availability" content="http://schema.org/InStock">In Stock</span>
  </div>
  
  <div itemprop="aggregateRating" itemscope itemtype="http://schema.org/AggregateRating">
    Rating: <span itemprop="ratingValue">4.8</span> out of 
    <span itemprop="bestRating">5</span> 
    (<span itemprop="ratingCount">24</span> reviews)
  </div>
</div>

<!-- Event information -->
<div itemscope itemtype="http://schema.org/Event">
  <h3 itemprop="name">Web Development Workshop</h3>
  
  <div itemprop="description">
    Learn modern web development techniques in this hands-on workshop.
  </div>
  
  <div>
    Date: <time itemprop="startDate" datetime="2024-01-15T09:00">
      January 15, 2024 at 9:00 AM
    </time>
  </div>
  
  <div itemprop="location" itemscope itemtype="http://schema.org/Place">
    <span itemprop="name">Tech Conference Center</span>
    <div itemprop="address" itemscope itemtype="http://schema.org/PostalAddress">
      <span itemprop="streetAddress">456 Conference Ave</span>,
      <span itemprop="addressLocality">Tech City</span>
    </div>
  </div>
  
  <div itemprop="offers" itemscope itemtype="http://schema.org/Offer">
    Price: $<span itemprop="price">199</span>
    <span itemprop="priceCurrency">USD</span>
  </div>
</div>

<!-- FAQ section -->
<div itemscope itemtype="http://schema.org/FAQPage">
  <h2>Frequently Asked Questions</h2>
  
  <div itemscope itemprop="mainEntity" itemtype="http://schema.org/Question">
    <h3 itemprop="name">What is semantic HTML?</h3>
    <div itemscope itemprop="acceptedAnswer" itemtype="http://schema.org/Answer">
      <div itemprop="text">
        Semantic HTML is the use of HTML markup to reinforce the semantics, 
        or meaning, of the information in webpages and web applications.
      </div>
    </div>
  </div>
  
  <div itemscope itemprop="mainEntity" itemtype="http://schema.org/Question">
    <h3 itemprop="name">Why is accessibility important?</h3>
    <div itemscope itemprop="acceptedAnswer" itemtype="http://schema.org/Answer">
      <div itemprop="text">
        Accessibility ensures that websites can be used by people with 
        disabilities, providing equal access to information and functionality.
      </div>
    </div>
  </div>
</div>
```

## Form Semantics {#forms}

### Accessible Form Design
```html
<form novalidate>
  <fieldset>
    <legend>Personal Information</legend>
    
    <div class="form-group">
      <label for="first-name">
        First Name <span aria-label="required">*</span>
      </label>
      <input type="text" 
             id="first-name" 
             name="firstName"
             required
             aria-describedby="first-name-error"
             aria-invalid="false">
      <div id="first-name-error" class="error-message" role="alert">
        <!-- Error message will appear here -->
      </div>
    </div>
    
    <div class="form-group">
      <label for="email">
        Email Address <span aria-label="required">*</span>
      </label>
      <input type="email" 
             id="email" 
             name="email"
             required
             aria-describedby="email-help email-error"
             autocomplete="email">
      <div id="email-help" class="help-text">
        We'll never share your email with anyone else.
      </div>
      <div id="email-error" class="error-message" role="alert">
        <!-- Error message will appear here -->
      </div>
    </div>
    
    <div class="form-group">
      <label for="phone">Phone Number</label>
      <input type="tel" 
             id="phone" 
             name="phone"
             aria-describedby="phone-help"
             autocomplete="tel">
      <div id="phone-help" class="help-text">
        Optional. Format: (123) 456-7890
      </div>
    </div>
  </fieldset>
  
  <fieldset>
    <legend>Preferences</legend>
    
    <div class="form-group">
      <fieldset>
        <legend>Notification Method</legend>
        
        <label>
          <input type="radio" name="notification" value="email" checked>
          Email notifications
        </label>
        
        <label>
          <input type="radio" name="notification" value="sms">
          SMS notifications
        </label>
        
        <label>
          <input type="radio" name="notification" value="none">
          No notifications
        </label>
      </fieldset>
    </div>
    
    <div class="form-group">
      <label>
        <input type="checkbox" name="newsletter" value="yes">
        Subscribe to our newsletter
      </label>
    </div>
    
    <div class="form-group">
      <label for="comments">Additional Comments</label>
      <textarea id="comments" 
                name="comments"
                rows="4"
                aria-describedby="comments-help"
                maxlength="500"></textarea>
      <div id="comments-help" class="help-text">
        Maximum 500 characters
      </div>
    </div>
  </fieldset>
  
  <div class="form-actions">
    <button type="submit">Submit Form</button>
    <button type="reset">Reset Form</button>
  </div>
</form>
```

### Form Validation and Error Handling
```html
<form id="contact-form" novalidate>
  <div class="form-summary" id="form-errors" role="alert" aria-live="polite">
    <!-- Form-level errors will appear here -->
  </div>
  
  <div class="form-group">
    <label for="username">Username</label>
    <input type="text" 
           id="username" 
           name="username"
           required
           minlength="3"
           maxlength="20"
           pattern="^[a-zA-Z0-9_]+$"
           aria-describedby="username-help username-error">
    <div id="username-help" class="help-text">
      3-20 characters, letters, numbers, and underscores only
    </div>
    <div id="username-error" class="error-message"></div>
  </div>
  
  <div class="form-group">
    <label for="password">Password</label>
    <input type="password" 
           id="password" 
           name="password"
           required
           minlength="8"
           aria-describedby="password-help password-error">
    <div id="password-help" class="help-text">
      Minimum 8 characters required
    </div>
    <div id="password-error" class="error-message"></div>
  </div>
  
  <button type="submit">Create Account</button>
</form>

<script>
// Enhanced form validation
document.getElementById('contact-form').addEventListener('submit', function(e) {
  e.preventDefault();
  
  const form = e.target;
  const errors = [];
  
  // Validate each field
  const fields = form.querySelectorAll('input[required]');
  fields.forEach(field => {
    const errorElement = document.getElementById(field.id + '-error');
    
    if (!field.validity.valid) {
      const error = getErrorMessage(field);
      errorElement.textContent = error;
      field.setAttribute('aria-invalid', 'true');
      errors.push(error);
    } else {
      errorElement.textContent = '';
      field.setAttribute('aria-invalid', 'false');
    }
  });
  
  // Display form-level errors
  const errorSummary = document.getElementById('form-errors');
  if (errors.length > 0) {
    errorSummary.innerHTML = `
      <h3>Please correct the following errors:</h3>
      <ul>${errors.map(error => `<li>${error}</li>`).join('')}</ul>
    `;
    errorSummary.focus();
  } else {
    errorSummary.innerHTML = '';
    // Submit form
    console.log('Form is valid, submitting...');
  }
});

function getErrorMessage(field) {
  if (field.validity.valueMissing) {
    return `${field.labels[0].textContent} is required`;
  }
  if (field.validity.tooShort) {
    return `${field.labels[0].textContent} must be at least ${field.minLength} characters`;
  }
  if (field.validity.patternMismatch) {
    return `${field.labels[0].textContent} format is invalid`;
  }
  return `${field.labels[0].textContent} is invalid`;
}
</script>
```

This comprehensive guide demonstrates how to build meaningful, accessible, and SEO-friendly web structures using HTML5 semantic elements. By following these patterns and best practices, you'll create websites that work better for all users, perform well in search engines, and are easier to maintain over time.

Remember that semantic HTML is not just about using the right tags—it's about understanding the meaning and purpose of your content and choosing markup that best represents that meaning. This approach benefits everyone: users with disabilities, search engines, developers, and even future versions of your own code.''',
            'category': 'HTML5',
            'tags': 'html5,semantic-web,accessibility,web-components',
        },
        {
            'title': 'CSS3 Mastery: Layouts & Effects',
            'content': '''# CSS3 Mastery: Layouts & Effects

## Introduction

CSS3 has revolutionized web design with powerful layout systems and visual effects that were previously impossible or required complex workarounds. This comprehensive guide explores advanced CSS3 techniques for creating sophisticated layouts and stunning visual effects that enhance user experience while maintaining performance and accessibility.

## Modern Layout Systems

### CSS Grid Layout

CSS Grid is the most powerful layout system available in CSS, providing two-dimensional control over both rows and columns.

#### Basic Grid Setup

```css
.grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    grid-gap: 20px;
    padding: 20px;
}

.grid-item {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 8px;
    color: white;
}
```

#### Advanced Grid Techniques

```css
.complex-grid {
    display: grid;
    grid-template-areas: 
        "header header header"
        "sidebar main aside"
        "footer footer footer";
    grid-template-columns: 200px 1fr 150px;
    grid-template-rows: auto 1fr auto;
    min-height: 100vh;
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }
.aside { grid-area: aside; }
.footer { grid-area: footer; }
```

#### Responsive Grid Systems

```css
.responsive-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
}

@media (max-width: 768px) {
    .responsive-grid {
        grid-template-columns: 1fr;
        gap: 1rem;
    }
}
```

### Flexbox Mastery

Flexbox excels at one-dimensional layouts and component alignment.

#### Advanced Flex Patterns

```css
.flex-card {
    display: flex;
    flex-direction: column;
    min-height: 400px;
}

.flex-card-header {
    flex: 0 0 auto;
    padding: 1rem;
    background: #f8f9fa;
}

.flex-card-body {
    flex: 1 1 auto;
    padding: 1rem;
    overflow-y: auto;
}

.flex-card-footer {
    flex: 0 0 auto;
    padding: 1rem;
    border-top: 1px solid #dee2e6;
}
```

#### Flex Navigation Patterns

```css
.nav-flex {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
}

.nav-brand {
    flex: 0 0 auto;
    font-weight: bold;
    font-size: 1.25rem;
}

.nav-links {
    display: flex;
    list-style: none;
    margin: 0;
    padding: 0;
    gap: 2rem;
}

.nav-actions {
    flex: 0 0 auto;
    display: flex;
    gap: 1rem;
}
```

## Advanced CSS Effects

### Transform and Animations

#### 3D Transformations

```css
.card-3d {
    perspective: 1000px;
    width: 300px;
    height: 200px;
}

.card-inner {
    position: relative;
    width: 100%;
    height: 100%;
    text-align: center;
    transition: transform 0.6s;
    transform-style: preserve-3d;
}

.card-3d:hover .card-inner {
    transform: rotateY(180deg);
}

.card-front, .card-back {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.card-back {
    transform: rotateY(180deg);
    background: linear-gradient(45deg, #667eea, #764ba2);
}
```

#### Complex Animations

```css
@keyframes morphShape {
    0% {
        border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
    }
    50% {
        border-radius: 30% 60% 70% 40% / 50% 60% 30% 60%;
        background: linear-gradient(45deg, #4ecdc4, #45b7d1);
    }
    100% {
        border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
        background: linear-gradient(45deg, #96ceb4, #ffeaa7);
    }
}

.morphing-blob {
    width: 200px;
    height: 200px;
    animation: morphShape 4s ease-in-out infinite;
    transition: all 0.3s ease;
}
```

#### Scroll-triggered Animations

```css
.fade-in-on-scroll {
    opacity: 0;
    transform: translateY(30px);
    transition: all 0.6s ease-out;
}

.fade-in-on-scroll.visible {
    opacity: 1;
    transform: translateY(0);
}

/* Using CSS scroll-timeline (experimental) */
@scroll-timeline slideIn {
    source: auto;
    orientation: vertical;
    scroll-offsets: 0px, 500px;
}

.scroll-animation {
    animation: slideInAnimation 1s linear slideIn;
}

@keyframes slideInAnimation {
    from { transform: translateX(-100%); }
    to { transform: translateX(0); }
}
```

### Advanced Visual Effects

#### CSS Filters and Blend Modes

```css
.image-effects {
    position: relative;
    overflow: hidden;
}

.image-effects img {
    transition: all 0.3s ease;
    filter: grayscale(0%) blur(0px) brightness(100%) contrast(100%);
}

.image-effects:hover img {
    filter: grayscale(30%) blur(2px) brightness(110%) contrast(120%);
    transform: scale(1.05);
}

.overlay-effect {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, rgba(255,107,107,0.8), rgba(78,205,196,0.8));
    opacity: 0;
    transition: opacity 0.3s ease;
    mix-blend-mode: multiply;
}

.image-effects:hover .overlay-effect {
    opacity: 1;
}
```

#### Advanced Shadow Effects

```css
.advanced-shadows {
    /* Neumorphism */
    background: #e0e5ec;
    border-radius: 20px;
    box-shadow: 
        9px 9px 16px #a3b1c6,
        -9px -9px 16px #ffffff;
    padding: 2rem;
}

.layered-shadows {
    box-shadow:
        0 1px 3px rgba(0,0,0,0.12),
        0 1px 2px rgba(0,0,0,0.24),
        0 3px 6px rgba(0,0,0,0.16),
        0 5px 10px rgba(0,0,0,0.19);
    transition: all 0.3s cubic-bezier(.25,.8,.25,1);
}

.layered-shadows:hover {
    box-shadow:
        0 14px 28px rgba(0,0,0,0.25),
        0 10px 10px rgba(0,0,0,0.22);
}
```

## Modern CSS Patterns

### CSS Custom Properties (Variables)

#### Dynamic Theming System

```css
:root {
    /* Color System */
    --primary-hue: 220;
    --primary-saturation: 90%;
    --primary-lightness: 60%;
    
    --primary: hsl(var(--primary-hue), var(--primary-saturation), var(--primary-lightness));
    --primary-light: hsl(var(--primary-hue), var(--primary-saturation), 70%);
    --primary-dark: hsl(var(--primary-hue), var(--primary-saturation), 40%);
    
    /* Spacing System */
    --space-xs: 0.25rem;
    --space-sm: 0.5rem;
    --space-md: 1rem;
    --space-lg: 1.5rem;
    --space-xl: 3rem;
    
    /* Typography */
    --font-scale: 1.25;
    --font-size-sm: calc(1rem / var(--font-scale));
    --font-size-md: 1rem;
    --font-size-lg: calc(1rem * var(--font-scale));
    --font-size-xl: calc(1rem * var(--font-scale) * var(--font-scale));
}

[data-theme="dark"] {
    --primary-lightness: 70%;
    --background: hsl(220, 10%, 10%);
    --text: hsl(220, 10%, 95%);
}

[data-theme="light"] {
    --background: hsl(220, 10%, 98%);
    --text: hsl(220, 10%, 10%);
}
```

#### Responsive Custom Properties

```css
:root {
    --container-padding: 1rem;
    --grid-columns: 1;
    --font-size-hero: 2rem;
}

@media (min-width: 768px) {
    :root {
        --container-padding: 2rem;
        --grid-columns: 2;
        --font-size-hero: 3rem;
    }
}

@media (min-width: 1024px) {
    :root {
        --container-padding: 3rem;
        --grid-columns: 3;
        --font-size-hero: 4rem;
    }
}

.container {
    padding: var(--container-padding);
}

.grid {
    display: grid;
    grid-template-columns: repeat(var(--grid-columns), 1fr);
}

.hero-title {
    font-size: var(--font-size-hero);
}
```

### Container Queries

```css
.card-container {
    container-type: inline-size;
    container-name: card;
}

.card {
    padding: 1rem;
    background: white;
    border-radius: 8px;
}

@container card (min-width: 300px) {
    .card {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .card-image {
        flex: 0 0 100px;
    }
    
    .card-content {
        flex: 1;
    }
}

@container card (min-width: 500px) {
    .card {
        padding: 2rem;
    }
    
    .card-title {
        font-size: 1.5rem;
    }
}
```

## Performance Optimization

### Hardware Acceleration

```css
.optimized-animation {
    /* Use transform and opacity for smooth animations */
    transform: translateZ(0); /* Force hardware acceleration */
    will-change: transform, opacity;
    transition: transform 0.3s ease, opacity 0.3s ease;
}

.smooth-scroll {
    overflow-y: scroll;
    scroll-behavior: smooth;
    /* Enable momentum scrolling on iOS */
    -webkit-overflow-scrolling: touch;
}
```

### Critical CSS Patterns

```css
/* Above-the-fold critical styles */
.hero-section {
    min-height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
}

/* Lazy-loaded styles */
.below-fold {
    opacity: 0;
    transform: translateY(20px);
    transition: all 0.6s ease;
}

.below-fold.loaded {
    opacity: 1;
    transform: translateY(0);
}
```

## Accessibility and CSS

### Focus Management

```css
.custom-button {
    position: relative;
    background: var(--primary);
    color: white;
    border: 2px solid transparent;
    border-radius: 4px;
    padding: 0.75rem 1.5rem;
    cursor: pointer;
    transition: all 0.2s ease;
}

.custom-button:focus-visible {
    outline: none;
    border-color: var(--focus-color, #4169E1);
    box-shadow: 0 0 0 2px rgba(65, 105, 225, 0.3);
}

.custom-button:hover:not(:disabled) {
    background: var(--primary-dark);
    transform: translateY(-1px);
}

.custom-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
}
```

### High Contrast Mode Support

```css
@media (prefers-contrast: high) {
    .card {
        border: 2px solid currentColor;
        background: ButtonFace;
        color: ButtonText;
    }
    
    .button {
        background: ButtonFace;
        color: ButtonText;
        border: 2px solid ButtonText;
    }
}

@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
```

## Browser Support and Fallbacks

### Progressive Enhancement

```css
.grid-fallback {
    /* Fallback for older browsers */
    display: flex;
    flex-wrap: wrap;
    margin: -10px;
}

.grid-fallback > * {
    flex: 1 1 300px;
    margin: 10px;
}

/* Enhanced version for modern browsers */
@supports (display: grid) {
    .grid-fallback {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        margin: 0;
    }
    
    .grid-fallback > * {
        margin: 0;
    }
}
```

### Feature Detection

```css
@supports (backdrop-filter: blur(10px)) {
    .glass-effect {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
}

@supports not (backdrop-filter: blur(10px)) {
    .glass-effect {
        background: rgba(255, 255, 255, 0.9);
    }
}
```

## Best Practices and Guidelines

### Naming Conventions

```css
/* BEM Methodology */
.component { }
.component__element { }
.component--modifier { }
.component__element--modifier { }

/* Utility Classes */
.u-text-center { text-align: center; }
.u-margin-bottom-large { margin-bottom: 3rem; }
.u-visually-hidden { 
    position: absolute !important;
    width: 1px !important;
    height: 1px !important;
    padding: 0 !important;
    margin: -1px !important;
    overflow: hidden !important;
    clip: rect(0,0,0,0) !important;
    white-space: nowrap !important;
    border: 0 !important;
}
```

### Code Organization

```css
/* Variables and Custom Properties */
:root { }

/* Base and Reset Styles */
*, *::before, *::after { }
html, body { }

/* Typography */
h1, h2, h3, h4, h5, h6 { }
p, ul, ol { }

/* Layout Components */
.container { }
.grid { }
.flex { }

/* UI Components */
.button { }
.card { }
.modal { }

/* Utilities */
.u-text-center { }
.u-margin-auto { }

/* States */
.is-active { }
.is-hidden { }
.is-loading { }
```

## Conclusion

CSS3 has evolved into a powerful toolkit for creating sophisticated layouts and stunning visual effects. By mastering Grid, Flexbox, custom properties, and modern CSS features, developers can create responsive, accessible, and performant web experiences. Remember to always consider browser support, accessibility, and performance when implementing advanced CSS techniques.

The key to CSS mastery lies in understanding when to use each tool and how to combine them effectively. Start with solid foundations, progressively enhance with advanced features, and always test across different devices and browsers to ensure a consistent user experience.''',
            'category': 'CSS3',
            'tags': 'css3,layout,animations,design-systems',
        },
        {
            'title': 'Go Concurrency Patterns',
            'content': '''# Go Concurrency Patterns

## Introduction

Go's concurrency model is one of its most powerful features, built around goroutines and channels that make concurrent programming more intuitive and safer than traditional thread-based approaches. This comprehensive guide explores advanced concurrency patterns that enable you to build scalable, efficient, and maintainable concurrent applications.

## Fundamental Concepts

### Goroutines vs Threads

Goroutines are lightweight, managed by the Go runtime, and much more efficient than OS threads:

```go
package main

import (
    "fmt"
    "runtime"
    "sync"
    "time"
)

func main() {
    fmt.Printf("Number of CPUs: %d\\n", runtime.NumCPU())
    fmt.Printf("Number of Goroutines: %d\\n", runtime.NumGoroutine())
    
    var wg sync.WaitGroup
    
    // Launch 10000 goroutines
    for i := 0; i < 10000; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            time.Sleep(time.Second)
            if id%1000 == 0 {
                fmt.Printf("Goroutine %d completed\\n", id)
            }
        }(i)
    }
    
    wg.Wait()
    fmt.Printf("Final Goroutines: %d\\n", runtime.NumGoroutine())
}
```

### Channel Fundamentals

Channels are the pipes that connect concurrent goroutines:

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    // Unbuffered channel
    messages := make(chan string)
    
    // Buffered channel
    buffered := make(chan int, 3)
    
    // Send and receive
    go func() {
        messages <- "Hello"
        messages <- "World"
        close(messages)
    }()
    
    // Range over channel
    for msg := range messages {
        fmt.Println(msg)
    }
    
    // Buffered channel usage
    buffered <- 1
    buffered <- 2
    buffered <- 3
    
    fmt.Println(<-buffered)
    fmt.Println(<-buffered)
    fmt.Println(<-buffered)
}
```

## Core Concurrency Patterns

### Worker Pool Pattern

The worker pool pattern distributes work across a fixed number of goroutines:

```go
package main

import (
    "fmt"
    "math/rand"
    "sync"
    "time"
)

type Job struct {
    ID     int
    Data   string
    Result chan string
}

type WorkerPool struct {
    workers   int
    jobQueue  chan Job
    wg        sync.WaitGroup
    quit      chan struct{}
}

func NewWorkerPool(workers int, queueSize int) *WorkerPool {
    return &WorkerPool{
        workers:  workers,
        jobQueue: make(chan Job, queueSize),
        quit:     make(chan struct{}),
    }
}

func (wp *WorkerPool) Start() {
    for i := 0; i < wp.workers; i++ {
        wp.wg.Add(1)
        go wp.worker(i)
    }
}

func (wp *WorkerPool) worker(id int) {
    defer wp.wg.Done()
    
    for {
        select {
        case job := <-wp.jobQueue:
            // Simulate work
            processingTime := time.Duration(rand.Intn(100)) * time.Millisecond
            time.Sleep(processingTime)
            
            result := fmt.Sprintf("Worker %d processed job %d: %s", id, job.ID, job.Data)
            job.Result <- result
            
        case <-wp.quit:
            fmt.Printf("Worker %d stopping\\n", id)
            return
        }
    }
}

func (wp *WorkerPool) Submit(job Job) {
    wp.jobQueue <- job
}

func (wp *WorkerPool) Stop() {
    close(wp.quit)
    wp.wg.Wait()
    close(wp.jobQueue)
}

func main() {
    pool := NewWorkerPool(5, 100)
    pool.Start()
    
    // Submit jobs
    for i := 0; i < 20; i++ {
        result := make(chan string, 1)
        job := Job{
            ID:     i,
            Data:   fmt.Sprintf("task-%d", i),
            Result: result,
        }
        
        pool.Submit(job)
        
        go func(jobID int) {
            select {
            case res := <-result:
                fmt.Printf("Job %d result: %s\\n", jobID, res)
            case <-time.After(time.Second):
                fmt.Printf("Job %d timed out\\n", jobID)
            }
        }(i)
    }
    
    time.Sleep(2 * time.Second)
    pool.Stop()
}
```

### Pipeline Pattern

Pipelines break down processing into stages connected by channels:

```go
package main

import (
    "fmt"
    "strings"
    "sync"
)

// Stage 1: Generate data
func generator(data []string) <-chan string {
    out := make(chan string)
    go func() {
        defer close(out)
        for _, item := range data {
            out <- item
        }
    }()
    return out
}

// Stage 2: Transform data
func transformer(in <-chan string) <-chan string {
    out := make(chan string)
    go func() {
        defer close(out)
        for item := range in {
            // Transform: convert to uppercase and add prefix
            transformed := fmt.Sprintf("PROCESSED: %s", strings.ToUpper(item))
            out <- transformed
        }
    }()
    return out
}

// Stage 3: Filter data
func filter(in <-chan string, pattern string) <-chan string {
    out := make(chan string)
    go func() {
        defer close(out)
        for item := range in {
            if strings.Contains(item, pattern) {
                out <- item
            }
        }
    }()
    return out
}

// Fan-out pattern: distribute work to multiple goroutines
func fanOut(in <-chan string, workers int) []<-chan string {
    outputs := make([]<-chan string, workers)
    
    for i := 0; i < workers; i++ {
        output := make(chan string)
        outputs[i] = output
        
        go func(out chan<- string) {
            defer close(out)
            for item := range in {
                // Simulate processing
                processed := fmt.Sprintf("Worker processed: %s", item)
                out <- processed
            }
        }(output)
    }
    
    return outputs
}

// Fan-in pattern: merge multiple channels into one
func fanIn(inputs ...<-chan string) <-chan string {
    out := make(chan string)
    var wg sync.WaitGroup
    
    for _, input := range inputs {
        wg.Add(1)
        go func(ch <-chan string) {
            defer wg.Done()
            for item := range ch {
                out <- item
            }
        }(input)
    }
    
    go func() {
        wg.Wait()
        close(out)
    }()
    
    return out
}

func main() {
    data := []string{
        "hello world",
        "golang programming",
        "concurrency patterns",
        "channel communication",
        "goroutine management",
    }
    
    // Build pipeline
    stage1 := generator(data)
    stage2 := transformer(stage1)
    stage3 := filter(stage2, "GOLANG")
    
    // Fan-out to multiple workers
    workers := fanOut(stage3, 3)
    
    // Fan-in results
    results := fanIn(workers...)
    
    // Collect results
    for result := range results {
        fmt.Println(result)
    }
}
```

### Producer-Consumer Pattern

```go
package main

import (
    "context"
    "fmt"
    "math/rand"
    "sync"
    "time"
)

type Message struct {
    ID        int
    Content   string
    Timestamp time.Time
}

type Producer struct {
    id       int
    output   chan<- Message
    quit     chan struct{}
    interval time.Duration
}

func NewProducer(id int, output chan<- Message, interval time.Duration) *Producer {
    return &Producer{
        id:       id,
        output:   output,
        quit:     make(chan struct{}),
        interval: interval,
    }
}

func (p *Producer) Start(ctx context.Context, wg *sync.WaitGroup) {
    defer wg.Done()
    ticker := time.NewTicker(p.interval)
    defer ticker.Stop()
    
    messageID := 0
    
    for {
        select {
        case <-ticker.C:
            msg := Message{
                ID:        messageID,
                Content:   fmt.Sprintf("Message from producer %d", p.id),
                Timestamp: time.Now(),
            }
            
            select {
            case p.output <- msg:
                fmt.Printf("Producer %d sent message %d\\n", p.id, messageID)
                messageID++
            case <-ctx.Done():
                fmt.Printf("Producer %d stopping due to context cancellation\\n", p.id)
                return
            }
            
        case <-ctx.Done():
            fmt.Printf("Producer %d stopping\\n", p.id)
            return
        }
    }
}

type Consumer struct {
    id    int
    input <-chan Message
}

func NewConsumer(id int, input <-chan Message) *Consumer {
    return &Consumer{
        id:    id,
        input: input,
    }
}

func (c *Consumer) Start(ctx context.Context, wg *sync.WaitGroup) {
    defer wg.Done()
    
    for {
        select {
        case msg, ok := <-c.input:
            if !ok {
                fmt.Printf("Consumer %d: input channel closed\\n", c.id)
                return
            }
            
            // Simulate processing time
            processingTime := time.Duration(rand.Intn(500)) * time.Millisecond
            time.Sleep(processingTime)
            
            fmt.Printf("Consumer %d processed message %d: %s (age: %v)\\n", 
                c.id, msg.ID, msg.Content, time.Since(msg.Timestamp))
                
        case <-ctx.Done():
            fmt.Printf("Consumer %d stopping\\n", c.id)
            return
        }
    }
}

func main() {
    ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
    defer cancel()
    
    // Create channel with buffer
    messageQueue := make(chan Message, 10)
    
    var wg sync.WaitGroup
    
    // Start producers
    numProducers := 2
    for i := 0; i < numProducers; i++ {
        producer := NewProducer(i, messageQueue, 500*time.Millisecond)
        wg.Add(1)
        go producer.Start(ctx, &wg)
    }
    
    // Start consumers
    numConsumers := 3
    for i := 0; i < numConsumers; i++ {
        consumer := NewConsumer(i, messageQueue)
        wg.Add(1)
        go consumer.Start(ctx, &wg)
    }
    
    // Wait for context to complete
    <-ctx.Done()
    
    // Close the message queue
    close(messageQueue)
    
    // Wait for all goroutines to finish
    wg.Wait()
    fmt.Println("All producers and consumers stopped")
}
```

## Advanced Patterns

### Rate Limiting

```go
package main

import (
    "context"
    "fmt"
    "sync"
    "time"
)

type RateLimiter struct {
    tokens chan struct{}
    ticker *time.Ticker
    quit   chan struct{}
}

func NewRateLimiter(rate int, burst int) *RateLimiter {
    rl := &RateLimiter{
        tokens: make(chan struct{}, burst),
        ticker: time.NewTicker(time.Second / time.Duration(rate)),
        quit:   make(chan struct{}),
    }
    
    // Fill initial burst
    for i := 0; i < burst; i++ {
        rl.tokens <- struct{}{}
    }
    
    // Start token refill
    go rl.refill()
    
    return rl
}

func (rl *RateLimiter) refill() {
    defer rl.ticker.Stop()
    
    for {
        select {
        case <-rl.ticker.C:
            select {
            case rl.tokens <- struct{}{}:
                // Token added
            default:
                // Bucket full, drop token
            }
        case <-rl.quit:
            return
        }
    }
}

func (rl *RateLimiter) Allow() bool {
    select {
    case <-rl.tokens:
        return true
    default:
        return false
    }
}

func (rl *RateLimiter) Wait(ctx context.Context) error {
    select {
    case <-rl.tokens:
        return nil
    case <-ctx.Done():
        return ctx.Err()
    }
}

func (rl *RateLimiter) Stop() {
    close(rl.quit)
}

// API request simulator
func makeAPIRequest(id int, rl *RateLimiter) error {
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()
    
    if err := rl.Wait(ctx); err != nil {
        return fmt.Errorf("rate limit wait failed: %w", err)
    }
    
    // Simulate API call
    fmt.Printf("Making API request %d at %s\\n", id, time.Now().Format("15:04:05.000"))
    time.Sleep(100 * time.Millisecond)
    
    return nil
}

func main() {
    // Allow 5 requests per second with burst of 10
    rateLimiter := NewRateLimiter(5, 10)
    defer rateLimiter.Stop()
    
    var wg sync.WaitGroup
    
    // Simulate 50 API requests
    for i := 0; i < 50; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            if err := makeAPIRequest(id, rateLimiter); err != nil {
                fmt.Printf("Request %d failed: %v\\n", id, err)
            }
        }(i)
    }
    
    wg.Wait()
    fmt.Println("All requests completed")
}
```

### Circuit Breaker Pattern

```go
package main

import (
    "context"
    "errors"
    "fmt"
    "math/rand"
    "sync"
    "time"
)

type State int

const (
    StateClosed State = iota
    StateHalfOpen
    StateOpen
)

type CircuitBreaker struct {
    mu                  sync.RWMutex
    state              State
    failureCount       int
    successCount       int
    failureThreshold   int
    successThreshold   int
    timeout           time.Duration
    lastFailureTime   time.Time
    nextAttempt       time.Time
}

func NewCircuitBreaker(failureThreshold, successThreshold int, timeout time.Duration) *CircuitBreaker {
    return &CircuitBreaker{
        state:            StateClosed,
        failureThreshold: failureThreshold,
        successThreshold: successThreshold,
        timeout:          timeout,
    }
}

func (cb *CircuitBreaker) Call(ctx context.Context, fn func() error) error {
    cb.mu.Lock()
    defer cb.mu.Unlock()
    
    if cb.state == StateOpen {
        if time.Now().Before(cb.nextAttempt) {
            return errors.New("circuit breaker is open")
        }
        cb.state = StateHalfOpen
        cb.successCount = 0
    }
    
    err := fn()
    
    if err != nil {
        cb.onFailure()
        return err
    }
    
    cb.onSuccess()
    return nil
}

func (cb *CircuitBreaker) onFailure() {
    cb.failureCount++
    cb.lastFailureTime = time.Now()
    
    if cb.state == StateHalfOpen || cb.failureCount >= cb.failureThreshold {
        cb.state = StateOpen
        cb.nextAttempt = time.Now().Add(cb.timeout)
        fmt.Printf("Circuit breaker opened at %s\\n", time.Now().Format("15:04:05"))
    }
}

func (cb *CircuitBreaker) onSuccess() {
    cb.failureCount = 0
    
    if cb.state == StateHalfOpen {
        cb.successCount++
        if cb.successCount >= cb.successThreshold {
            cb.state = StateClosed
            fmt.Printf("Circuit breaker closed at %s\\n", time.Now().Format("15:04:05"))
        }
    }
}

func (cb *CircuitBreaker) GetState() State {
    cb.mu.RLock()
    defer cb.mu.RUnlock()
    return cb.state
}

// Simulate an unreliable service
func unreliableService() error {
    // 30% chance of failure
    if rand.Float32() < 0.3 {
        return errors.New("service failure")
    }
    
    // Simulate network delay
    time.Sleep(time.Duration(rand.Intn(100)) * time.Millisecond)
    return nil
}

func main() {
    cb := NewCircuitBreaker(3, 2, 5*time.Second)
    
    var wg sync.WaitGroup
    
    // Simulate 100 service calls
    for i := 0; i < 100; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            
            ctx, cancel := context.WithTimeout(context.Background(), time.Second)
            defer cancel()
            
            err := cb.Call(ctx, unreliableService)
            
            state := cb.GetState()
            stateStr := map[State]string{
                StateClosed:   "CLOSED",
                StateHalfOpen: "HALF-OPEN",
                StateOpen:     "OPEN",
            }
            
            if err != nil {
                fmt.Printf("Call %d failed: %v (state: %s)\\n", id, err, stateStr[state])
            } else {
                fmt.Printf("Call %d succeeded (state: %s)\\n", id, stateStr[state])
            }
        }(i)
        
        time.Sleep(100 * time.Millisecond)
    }
    
    wg.Wait()
}
```

## Error Handling and Graceful Shutdown

### Context-based Cancellation

```go
package main

import (
    "context"
    "fmt"
    "os"
    "os/signal"
    "sync"
    "syscall"
    "time"
)

type Server struct {
    name string
    wg   sync.WaitGroup
}

func (s *Server) Start(ctx context.Context) {
    s.wg.Add(1)
    go s.run(ctx)
}

func (s *Server) run(ctx context.Context) {
    defer s.wg.Done()
    
    ticker := time.NewTicker(time.Second)
    defer ticker.Stop()
    
    fmt.Printf("%s started\\n", s.name)
    
    for {
        select {
        case <-ticker.C:
            fmt.Printf("%s: heartbeat at %s\\n", s.name, time.Now().Format("15:04:05"))
        case <-ctx.Done():
            fmt.Printf("%s: received shutdown signal\\n", s.name)
            
            // Simulate cleanup time
            time.Sleep(2 * time.Second)
            fmt.Printf("%s: cleanup completed\\n", s.name)
            return
        }
    }
}

func (s *Server) Stop() {
    s.wg.Wait()
    fmt.Printf("%s: stopped\\n", s.name)
}

func main() {
    // Create context that cancels on interrupt
    ctx, cancel := context.WithCancel(context.Background())
    
    // Handle OS signals
    sigChan := make(chan os.Signal, 1)
    signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)
    
    // Start multiple servers
    servers := []*Server{
        {name: "HTTP Server"},
        {name: "gRPC Server"},
        {name: "Background Worker"},
    }
    
    for _, server := range servers {
        server.Start(ctx)
    }
    
    // Wait for signal
    sig := <-sigChan
    fmt.Printf("\\nReceived signal: %v\\n", sig)
    
    // Cancel context to trigger graceful shutdown
    cancel()
    
    // Wait for all servers to stop
    for _, server := range servers {
        server.Stop()
    }
    
    fmt.Println("Application shutdown complete")
}
```

## Performance Monitoring and Debugging

### Goroutine Monitoring

```go
package main

import (
    "fmt"
    "runtime"
    "sync"
    "time"
)

type Monitor struct {
    ticker *time.Ticker
    quit   chan struct{}
}

func NewMonitor(interval time.Duration) *Monitor {
    return &Monitor{
        ticker: time.NewTicker(interval),
        quit:   make(chan struct{}),
    }
}

func (m *Monitor) Start() {
    go func() {
        for {
            select {
            case <-m.ticker.C:
                m.printStats()
            case <-m.quit:
                m.ticker.Stop()
                return
            }
        }
    }()
}

func (m *Monitor) Stop() {
    close(m.quit)
}

func (m *Monitor) printStats() {
    var memStats runtime.MemStats
    runtime.ReadMemStats(&memStats)
    
    fmt.Printf("=== Runtime Stats ===\\n")
    fmt.Printf("Goroutines: %d\\n", runtime.NumGoroutine())
    fmt.Printf("CPUs: %d\\n", runtime.NumCPU())
    fmt.Printf("Memory Alloc: %d KB\\n", memStats.Alloc/1024)
    fmt.Printf("Total Alloc: %d KB\\n", memStats.TotalAlloc/1024)
    fmt.Printf("GC Cycles: %d\\n", memStats.NumGC)
    fmt.Println("====================")
}

// Simulate workload
func worker(id int, wg *sync.WaitGroup, duration time.Duration) {
    defer wg.Done()
    
    fmt.Printf("Worker %d started\\n", id)
    
    // Simulate memory allocation
    data := make([]byte, 1024*1024) // 1MB
    
    for i := 0; i < len(data); i++ {
        data[i] = byte(i % 256)
    }
    
    time.Sleep(duration)
    fmt.Printf("Worker %d finished\\n", id)
}

func main() {
    monitor := NewMonitor(2 * time.Second)
    monitor.Start()
    defer monitor.Stop()
    
    var wg sync.WaitGroup
    
    // Launch workers in waves
    for wave := 0; wave < 3; wave++ {
        fmt.Printf("\\n=== Starting wave %d ===\\n", wave+1)
        
        for i := 0; i < 10; i++ {
            wg.Add(1)
            go worker(wave*10+i, &wg, time.Duration(2+wave)*time.Second)
        }
        
        time.Sleep(time.Second)
    }
    
    wg.Wait()
    
    // Force garbage collection
    runtime.GC()
    time.Sleep(time.Second)
    
    fmt.Println("\\nAll workers completed")
}
```

## Best Practices and Anti-patterns

### Memory Leaks Prevention

```go
package main

import (
    "context"
    "fmt"
    "sync"
    "time"
)

// BAD: Goroutine leak
func badPattern() {
    for i := 0; i < 10; i++ {
        go func(id int) {
            // This goroutine will run forever
            for {
                fmt.Printf("Goroutine %d running\\n", id)
                time.Sleep(time.Second)
            }
        }(i)
    }
}

// GOOD: Proper cleanup with context
func goodPattern(ctx context.Context) {
    var wg sync.WaitGroup
    
    for i := 0; i < 10; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            
            ticker := time.NewTicker(time.Second)
            defer ticker.Stop()
            
            for {
                select {
                case <-ticker.C:
                    fmt.Printf("Goroutine %d running\\n", id)
                case <-ctx.Done():
                    fmt.Printf("Goroutine %d stopping\\n", id)
                    return
                }
            }
        }(i)
    }
    
    wg.Wait()
}

// Channel cleanup patterns
func channelCleanupExample() {
    ch := make(chan int, 10)
    
    // Producer
    go func() {
        defer close(ch) // Always close channels when done
        for i := 0; i < 5; i++ {
            ch <- i
        }
    }()
    
    // Consumer
    for value := range ch {
        fmt.Printf("Received: %d\\n", value)
    }
}

func main() {
    fmt.Println("=== Good Pattern Example ===")
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()
    
    goodPattern(ctx)
    
    fmt.Println("\\n=== Channel Cleanup Example ===")
    channelCleanupExample()
}
```

## Conclusion

Go's concurrency model provides powerful primitives for building scalable applications. The key patterns covered in this guide—worker pools, pipelines, producer-consumer, rate limiting, and circuit breakers—form the foundation for most concurrent systems.

Remember these essential principles:

1. **Always provide cleanup mechanisms** using context cancellation
2. **Avoid goroutine leaks** by ensuring all goroutines can terminate
3. **Use buffered channels appropriately** to prevent blocking
4. **Monitor your concurrent systems** to detect issues early
5. **Test concurrent code thoroughly** including race conditions and deadlocks

Master these patterns and you'll be able to build robust, efficient concurrent applications that can handle real-world workloads while maintaining code clarity and maintainability.''',
            'category': 'Go',
            'tags': 'golang,concurrency,channels,patterns',
        }
    ]
    
    created_count = 0
    for article_data in articles_data:
        # Get category ID
        category_id = categories.get(article_data['category'])
        if not category_id:
            print(f"Warning: Category '{article_data['category']}' not found")
            continue
            
        # Check if article already exists
        existing = WikiArticle.query.filter_by(title=article_data['title']).first()
        if existing:
            print(f"Article already exists: {article_data['title']}")
            continue
            
        # Create article
        article = WikiArticle(
            title=article_data['title'],
            content=article_data['content'],
            category_id=category_id,
            tags=article_data['tags']
        )
        
        db.session.add(article)
        created_count += 1
        print(f"Created article: {article_data['title']}")
    
    db.session.commit()
    print(f"\nCreated {created_count} new articles")

def main():
    """Main function to create wiki content"""
    with app.app_context():
        print("Creating wiki categories...")
        categories = create_categories()
        
        print("\nCreating wiki articles...")
        create_articles(categories)
        
        print("\nWiki content creation completed!")

if __name__ == "__main__":
    main()
