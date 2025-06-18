#!/usr/bin/env python3
"""
Sample data for Wiki section - Categories and Articles
"""

from database import db
from models import WikiCategory, WikiArticle
from datetime import datetime, timedelta
import random

def populate_wiki_sample_data():
    """Populate sample wiki categories and articles"""
    
    print("📚 Populating Wiki section sample data...")
    
    # Check if categories already exist
    if WikiCategory.query.first():
        print("📋 Wiki categories already exist, skipping...")
    else:
        # Create sample categories (simplified to match your model)
        categories = [
            {
                'name': 'Web Development',
                'description': 'Frontend and backend web development tutorials, frameworks, and best practices'
            },
            {
                'name': 'Python Programming',
                'description': 'Python tutorials, libraries, frameworks, and advanced concepts'
            },
            {
                'name': 'Machine Learning',
                'description': 'AI/ML algorithms, data science, and practical implementations'
            },
            {
                'name': 'DevOps & Cloud',
                'description': 'Infrastructure, deployment, CI/CD, and cloud computing'
            },
            {
                'name': 'Database Systems',
                'description': 'SQL, NoSQL, database design, optimization, and management'
            },
            {
                'name': 'Software Engineering',
                'description': 'Design patterns, architecture, testing, and development methodologies'
            },
            {
                'name': 'Mobile Development',
                'description': 'iOS, Android, and cross-platform mobile app development'
            },
            {
                'name': 'Data Structures & Algorithms',
                'description': 'Computer science fundamentals, problem-solving, and optimization'
            }
        ]
        
        # Create category objects
        for cat_data in categories:
            category = WikiCategory(
                name=cat_data['name'],
                description=cat_data['description']
            )
            db.session.add(category)
        
        db.session.commit()
        print("✅ Created wiki categories")
    
    # Get existing categories
    web_dev = WikiCategory.query.filter_by(name='Web Development').first()
    python = WikiCategory.query.filter_by(name='Python Programming').first()
    ml = WikiCategory.query.filter_by(name='Machine Learning').first()
    devops = WikiCategory.query.filter_by(name='DevOps & Cloud').first()
    database = WikiCategory.query.filter_by(name='Database Systems').first()
    software_eng = WikiCategory.query.filter_by(name='Software Engineering').first()
    mobile = WikiCategory.query.filter_by(name='Mobile Development').first()
    algorithms = WikiCategory.query.filter_by(name='Data Structures & Algorithms').first()
    
    # Update existing articles with summaries if they don't have them
    existing_articles = WikiArticle.query.filter(
        db.or_(WikiArticle.summary.is_(None), WikiArticle.summary == '')
    ).all()
    
    if existing_articles:
        print("📝 Updating existing articles with summaries...")
        
        # Sample summaries for different topics
        sample_summaries = {
            'Flask': 'Learn to build modern web applications with Flask, including database integration, routing, and deployment best practices.',
            'JavaScript': 'Master JavaScript fundamentals and advanced concepts for building interactive web applications and modern user interfaces.',
            'Python': 'Comprehensive guide to Python programming, covering syntax, libraries, frameworks, and real-world applications.',
            'Docker': 'Learn containerization with Docker, including best practices for Python applications and production deployment.',
            'PostgreSQL': 'Complete guide to PostgreSQL performance optimization, indexing strategies, and database management techniques.',
            'Machine Learning': 'Introduction to machine learning concepts, algorithms, and practical implementations using Python and popular libraries.',
            'React': 'Build modern user interfaces with React, covering components, state management, and advanced patterns.',
            'API': 'Learn to design and build RESTful APIs with proper authentication, validation, and documentation.',
            'Git': 'Master version control with Git, including branching strategies, collaboration workflows, and best practices.',
            'Testing': 'Comprehensive guide to software testing, including unit tests, integration tests, and test-driven development.'
        }
        
        for article in existing_articles:
            # Generate summary based on title keywords
            summary = None
            for keyword, default_summary in sample_summaries.items():
                if keyword.lower() in article.title.lower():
                    summary = default_summary
                    break
            
            if not summary:
                # Generate summary from content if available
                if article.content:
                    # Extract first paragraph or create generic summary
                    clean_content = article.strip_html(article.content)
                    if len(clean_content) > 100:
                        summary = clean_content[:200] + '...'
                    else:
                        summary = clean_content or 'Explore this comprehensive guide covering important concepts and practical applications.'
                else:
                    summary = 'Discover valuable insights and practical knowledge in this comprehensive article.'
            
            article.summary = summary
            
        db.session.commit()
        print(f"✅ Updated {len(existing_articles)} articles with summaries")
    
    # Check if articles already exist
    if WikiArticle.query.first():
        print("📄 Wiki articles already exist, updating existing ones...")
        
        # Update existing articles with category assignments
        articles = WikiArticle.query.all()
        categories_list = [web_dev, python, ml, devops, database, software_eng, mobile, algorithms]
        
        for i, article in enumerate(articles):
            if article.category_id is None:
                # Assign categories in round-robin fashion
                if categories_list:
                    article.category_id = categories_list[i % len(categories_list)].id
        
        db.session.commit()
        print("✅ Updated existing articles with categories")
    
    else:
        # Create sample articles
        sample_articles = [
            # Web Development Articles
            {
                'title': 'Building Modern Web Applications with Flask',
                'content': '''
                <h2>Introduction to Flask</h2>
                <p>Flask is a lightweight Python web framework that provides a solid foundation for building web applications. In this comprehensive guide, we'll explore how to create modern, scalable web applications using Flask.</p>
                
                <h3>Setting Up Your Flask Environment</h3>
                <pre><code>pip install flask
pip install flask-sqlalchemy
pip install flask-migrate</code></pre>
                
                <h3>Creating Your First Flask App</h3>
                <p>Let's start with a simple Flask application structure:</p>
                <pre><code>from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)</code></pre>
                
                <h3>Database Integration</h3>
                <p>Flask-SQLAlchemy provides an excellent ORM for database operations. Here's how to set it up:</p>
                <pre><code>from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)</code></pre>
                
                <h3>Creating Models</h3>
                <p>Define your database models using SQLAlchemy:</p>
                <pre><code>class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)</code></pre>
                
                <h3>Deployment Considerations</h3>
                <p>When deploying Flask applications, consider using production WSGI servers like Gunicorn or uWSGI, and implement proper error handling and logging.</p>
                ''',
                'summary': 'Learn how to build modern web applications using Flask, from basic setup to advanced features like database integration and deployment.',
                'category_id': web_dev.id if web_dev else None,
                'tags': 'flask, python, web-development, tutorial'
            },
            {
                'title': 'CSS Grid vs Flexbox: When to Use What',
                'content': '''
                <h2>Understanding CSS Layout Systems</h2>
                <p>CSS Grid and Flexbox are two powerful layout systems that solve different problems. This guide will help you understand when to use each.</p>
                
                <h3>CSS Flexbox</h3>
                <p>Flexbox is designed for one-dimensional layouts (either row or column). It's perfect for:</p>
                <ul>
                    <li>Navigation bars</li>
                    <li>Centering content</li>
                    <li>Distributing space between items</li>
                </ul>
                
                <pre><code>.container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}</code></pre>
                
                <h3>CSS Grid</h3>
                <p>Grid is perfect for two-dimensional layouts. Use it for:</p>
                <ul>
                    <li>Page layouts</li>
                    <li>Card-based designs</li>
                    <li>Complex responsive layouts</li>
                </ul>
                
                <pre><code>.grid-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}</code></pre>
                
                <h3>When to Use Each</h3>
                <p><strong>Use Flexbox when:</strong> You need to arrange items in a single dimension and want flexibility in how space is distributed.</p>
                <p><strong>Use Grid when:</strong> You need to create complex two-dimensional layouts with precise control over rows and columns.</p>
                ''',
                'summary': 'Master the differences between CSS Grid and Flexbox to choose the right layout system for your projects.',
                'category_id': web_dev.id if web_dev else None,
                'tags': 'css, flexbox, grid, layout, frontend'
            },
            
            # Python Programming Articles
            {
                'title': 'Python Decorators: A Complete Guide',
                'content': '''
                <h2>Understanding Python Decorators</h2>
                <p>Decorators are a powerful feature in Python that allow you to modify or enhance functions and classes without permanently modifying their code.</p>
                
                <h3>Basic Decorator Syntax</h3>
                <pre><code>def my_decorator(func):
    def wrapper():
        print("Before function call")
        func()
        print("After function call")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

# When you call say_hello(), it will print:
# Before function call
# Hello!
# After function call</code></pre>
                
                <h3>Decorators with Arguments</h3>
                <pre><code>def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"Hello, {name}!")</code></pre>
                
                <h3>Class Decorators</h3>
                <p>You can also use decorators on classes:</p>
                <pre><code>def add_repr(cls):
    def __repr__(self):
        return f"{cls.__name__}({', '.join(f'{k}={v}' for k, v in self.__dict__.items())})"
    cls.__repr__ = __repr__
    return cls

@add_repr
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age</code></pre>
                
                <h3>Real-World Use Cases</h3>
                <ul>
                    <li>Logging function calls</li>
                    <li>Measuring execution time</li>
                    <li>Authentication and authorization</li>
                    <li>Caching results</li>
                    <li>Input validation</li>
                </ul>
                ''',
                'summary': 'Master Python decorators with practical examples and real-world use cases.',
                'category_id': python.id if python else None,
                'tags': 'python, decorators, advanced, functions'
            },
            {
                'title': 'Async/Await in Python: Mastering Asynchronous Programming',
                'content': '''
                <h2>Introduction to Asyncio</h2>
                <p>Python's asyncio library enables you to write asynchronous, concurrent code using async/await syntax. This is particularly useful for I/O-heavy applications.</p>
                
                <h3>Basic Async Function</h3>
                <pre><code>import asyncio

async def fetch_data():
    print("Fetching data...")
    await asyncio.sleep(1)  # Simulate async operation
    return "Data fetched"

async def main():
    result = await fetch_data()
    print(result)

# Run the async function
asyncio.run(main())</code></pre>
                
                <h3>Running Multiple Async Tasks</h3>
                <pre><code>async def fetch_multiple():
    tasks = [
        fetch_data(),
        fetch_data(),
        fetch_data()
    ]
    results = await asyncio.gather(*tasks)
    return results</code></pre>
                
                <h3>Async Context Managers</h3>
                <pre><code>class AsyncDatabaseConnection:
    async def __aenter__(self):
        print("Connecting to database...")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Closing database connection...")

async def use_database():
    async with AsyncDatabaseConnection() as conn:
        # Use the connection
        pass</code></pre>
                
                <h3>When to Use Async/Await</h3>
                <ul>
                    <li>Making HTTP requests</li>
                    <li>Database operations</li>
                    <li>File I/O operations</li>
                    <li>Network operations</li>
                    <li>Any I/O-bound tasks</li>
                </ul>
                ''',
                'summary': 'Learn asynchronous programming in Python with practical examples and best practices.',
                'category_id': python.id if python else None,
                'tags': 'python, async, asyncio, concurrency'
            },
            
            # Machine Learning Articles
            {
                'title': 'Introduction to Neural Networks with PyTorch',
                'content': '''
                <h2>Getting Started with PyTorch</h2>
                <p>PyTorch is a popular deep learning framework that provides dynamic computation graphs and intuitive Python APIs.</p>
                
                <h3>Installing PyTorch</h3>
                <pre><code>pip install torch torchvision torchaudio</code></pre>
                
                <h3>Creating Your First Neural Network</h3>
                <pre><code>import torch
import torch.nn as nn
import torch.optim as optim

class SimpleNet(nn.Module):
    def __init__(self):
        super(SimpleNet, self).__init__()
        self.fc1 = nn.Linear(784, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 10)
        self.relu = nn.ReLU()
        
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# Create the model
model = SimpleNet()
print(model)</code></pre>
                
                <h3>Training the Model</h3>
                <pre><code># Define loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
for epoch in range(100):
    # Forward pass
    outputs = model(inputs)
    loss = criterion(outputs, targets)
    
    # Backward pass
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    if epoch % 10 == 0:
        print(f'Epoch {epoch}, Loss: {loss.item()}')</code></pre>
                
                <h3>Key Concepts</h3>
                <ul>
                    <li>Tensors: Multi-dimensional arrays</li>
                    <li>Autograd: Automatic differentiation</li>
                    <li>nn.Module: Base class for neural networks</li>
                    <li>Optimizers: Algorithms for updating weights</li>
                    <li>Loss functions: Measure prediction accuracy</li>
                </ul>
                ''',
                'summary': 'Build your first neural network using PyTorch with step-by-step instructions.',
                'category_id': ml.id if ml else None,
                'tags': 'pytorch, neural-networks, deep-learning, ai'
            },
            
            # DevOps Articles
            {
                'title': 'Docker Best Practices for Python Applications',
                'content': '''
                <h2>Containerizing Python Applications</h2>
                <p>Docker provides an excellent way to package and deploy Python applications consistently across environments.</p>
                
                <h3>Multi-stage Dockerfile</h3>
                <pre><code># Multi-stage build for smaller images
FROM python:3.9-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.9-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000
CMD ["python", "app.py"]</code></pre>
                
                <h3>Optimizing Docker Images</h3>
                <ul>
                    <li>Use multi-stage builds</li>
                    <li>Minimize layers</li>
                    <li>Use .dockerignore</li>
                    <li>Choose appropriate base images</li>
                    <li>Remove unnecessary packages</li>
                </ul>
                
                <h3>Docker Compose Example</h3>
                <pre><code>version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
    depends_on:
      - db
  
  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=mydb
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:</code></pre>
                
                <h3>Security Best Practices</h3>
                <ul>
                    <li>Don't run as root user</li>
                    <li>Use specific image tags</li>
                    <li>Scan for vulnerabilities</li>
                    <li>Keep base images updated</li>
                    <li>Use secrets management</li>
                </ul>
                ''',
                'summary': 'Learn Docker best practices specifically for Python applications, including multi-stage builds and optimization.',
                'category_id': devops.id if devops else None,
                'tags': 'docker, python, containerization, devops'
            },
            
            # Database Articles
            {
                'title': 'PostgreSQL Performance Optimization Guide',
                'content': '''
                <h2>Optimizing PostgreSQL Performance</h2>
                <p>Learn how to optimize your PostgreSQL database for better performance and scalability.</p>
                
                <h3>Indexing Strategies</h3>
                <pre><code>-- Create a B-tree index (default)
CREATE INDEX idx_user_email ON users(email);

-- Create a partial index
CREATE INDEX idx_active_users ON users(created_at) 
WHERE active = true;

-- Create a composite index
CREATE INDEX idx_user_name_email ON users(last_name, first_name, email);

-- Create a functional index
CREATE INDEX idx_user_email_lower ON users(LOWER(email));</code></pre>
                
                <h3>Query Optimization</h3>
                <pre><code>-- Use EXPLAIN ANALYZE to understand query performance
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'user@example.com';

-- Use EXPLAIN (BUFFERS, ANALYZE) for more detailed information
EXPLAIN (BUFFERS, ANALYZE) 
SELECT u.name, p.title 
FROM users u 
JOIN posts p ON u.id = p.user_id 
WHERE u.active = true;</code></pre>
                
                <h3>Configuration Tuning</h3>
                <pre><code># postgresql.conf optimizations
shared_buffers = 256MB          # 25% of total RAM
effective_cache_size = 1GB      # 75% of total RAM
work_mem = 4MB                  # Per-operation memory
maintenance_work_mem = 64MB     # For maintenance operations
checkpoint_completion_target = 0.9
wal_buffers = 16MB</code></pre>
                
                <h3>Monitoring and Maintenance</h3>
                <ul>
                    <li>Regular VACUUM and ANALYZE</li>
                    <li>Monitor slow queries</li>
                    <li>Check index usage</li>
                    <li>Monitor connection pools</li>
                    <li>Set up proper logging</li>
                </ul>
                ''',
                'summary': 'Comprehensive guide to PostgreSQL performance optimization, indexing, and query tuning.',
                'category_id': database.id if database else None,
                'tags': 'postgresql, database, optimization, performance'
            },
            
            # Software Engineering Articles
            {
                'title': 'SOLID Principles in Python',
                'content': '''
                <h2>Writing Better Code with SOLID Principles</h2>
                <p>The SOLID principles are five design principles that help create maintainable, scalable software.</p>
                
                <h3>Single Responsibility Principle (SRP)</h3>
                <p>A class should have only one reason to change.</p>
                <pre><code># Bad - Multiple responsibilities
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def save_to_database(self):
        # Database logic
        pass
    
    def send_email(self):
        # Email logic
        pass

# Good - Separated responsibilities
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class UserRepository:
    def save(self, user):
        # Database logic
        pass

class EmailService:
    def send_email(self, user, message):
        # Email logic
        pass</code></pre>
                
                <h3>Open/Closed Principle (OCP)</h3>
                <p>Classes should be open for extension but closed for modification.</p>
                <pre><code>from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass

class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount):
        print(f"Processing ${amount} via Credit Card")

class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount):
        print(f"Processing ${amount} via PayPal")</code></pre>
                
                <h3>Liskov Substitution Principle (LSP)</h3>
                <p>Objects of a superclass should be replaceable with objects of a subclass.</p>
                
                <h3>Interface Segregation Principle (ISP)</h3>
                <p>Clients should not be forced to depend on interfaces they don't use.</p>
                
                <h3>Dependency Inversion Principle (DIP)</h3>
                <p>High-level modules should not depend on low-level modules. Both should depend on abstractions.</p>
                
                <pre><code>class OrderService:
    def __init__(self, payment_processor: PaymentProcessor):
        self.payment_processor = payment_processor
    
    def process_order(self, order):
        # Process order logic
        self.payment_processor.process_payment(order.total)</code></pre>
                ''',
                'summary': 'Learn the SOLID principles with Python examples to write better, more maintainable code.',
                'category_id': software_eng.id if software_eng else None,
                'tags': 'solid, design-patterns, python, software-engineering'
            },
            
            # Algorithms Articles
            {
                'title': 'Dynamic Programming: From Beginner to Expert',
                'content': '''
                <h2>Understanding Dynamic Programming</h2>
                <p>Dynamic programming is an algorithmic technique for solving optimization problems by breaking them down into simpler subproblems.</p>
                
                <h3>Key Concepts</h3>
                <ul>
                    <li><strong>Optimal Substructure:</strong> Optimal solution contains optimal solutions to subproblems</li>
                    <li><strong>Overlapping Subproblems:</strong> Same subproblems solved multiple times</li>
                    <li><strong>Memoization:</strong> Store results to avoid recomputation</li>
                </ul>
                
                <h3>Fibonacci with Memoization</h3>
                <pre><code># Naive recursive approach (inefficient)
def fibonacci_naive(n):
    if n <= 1:
        return n
    return fibonacci_naive(n-1) + fibonacci_naive(n-2)

# Dynamic programming with memoization
def fibonacci_dp(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fibonacci_dp(n-1, memo) + fibonacci_dp(n-2, memo)
    return memo[n]

# Bottom-up approach
def fibonacci_bottom_up(n):
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]</code></pre>
                
                <h3>Longest Common Subsequence</h3>
                <pre><code>def lcs(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]</code></pre>
                
                <h3>Knapsack Problem</h3>
                <pre><code>def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(
                    dp[i-1][w],
                    dp[i-1][w-weights[i-1]] + values[i-1]
                )
            else:
                dp[i][w] = dp[i-1][w]
    
    return dp[n][capacity]</code></pre>
                
                <h3>Problem-Solving Strategy</h3>
                <ol>
                    <li>Identify if the problem has optimal substructure</li>
                    <li>Check for overlapping subproblems</li>
                    <li>Define the recurrence relation</li>
                    <li>Implement memoization or bottom-up approach</li>
                    <li>Optimize space complexity if possible</li>
                </ol>
                ''',
                'summary': 'Master dynamic programming with practical examples and problem-solving strategies.',
                'category_id': algorithms.id if algorithms else None,
                'tags': 'algorithms, dynamic-programming, optimization, problem-solving'
            }
        ]
        
        # Create articles with staggered creation dates
        base_date = datetime.now() - timedelta(days=30)
        
        for i, article_data in enumerate(sample_articles):
            # Stagger creation dates
            created_date = base_date + timedelta(days=i*3, hours=random.randint(1, 23))
            updated_date = created_date + timedelta(days=random.randint(1, 5))
            
            article = WikiArticle(
                title=article_data['title'],
                content=article_data['content'],
                category_id=article_data['category_id'],
                tags=article_data['tags'],
                created_at=created_date,
                updated_at=updated_date
            )
            db.session.add(article)
        
        db.session.commit()
        print("✅ Created sample wiki articles")
    
    print("🎉 Wiki section sample data populated successfully!")

if __name__ == '__main__':
    from app import app
    
    with app.app_context():
        populate_wiki_sample_data()