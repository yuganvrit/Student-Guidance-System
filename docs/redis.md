# JUNIOR DJANGO DEVELOPER - COMPLETE STUDY GUIDE
================================================================================
Redis for Django Developers
================================================================================

## 📋 TABLE OF CONTENTS
1. Must-Learn Redis Basics
2. When to Use What
3. Project Scenarios
4. Step-by-Step Implementation Guide
5. Common Patterns & Best Practices
6. Troubleshooting Checklist
7. Quick Reference Cheatsheet

================================================================================
1. MUST-LEARN REDIS BASICS (For Junior Developers)
================================================================================

## 🔴 LEVEL 1: ABSOLUTELY ESSENTIAL (2-3 hours)

### Installation & Setup
```bash
# Install Redis
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS
brew install redis

# Windows (using Docker)
docker run -d -p 6379:6379 redis

# Start Redis
redis-server

# Verify it's running
redis-cli ping  # Should return PONG
```

### Django Configuration
```python
# settings.py - EVERYTHING you need to start

# 1. Install package
# pip install django-redis redis hiredis

# 2. Basic Cache Setup
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'myapp',
        'TIMEOUT': 300,  # 5 minutes default
    }
}

# 3. Optional: Use Redis for sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
```

### Core Operations (90% of what you'll use)
```python
from django.core.cache import cache

# -------- GET/SET (Most Common - 50% of usage) --------
# Set a value with timeout
cache.set('user:1:name', 'John Doe', timeout=3600)

# Get a value
name = cache.get('user:1:name')

# Get with default if missing
name = cache.get('user:1:name', 'Guest')

# -------- DELETE (15% of usage) --------
cache.delete('user:1:name')

# -------- INCREMENT/DECREMENT (10% of usage) --------
cache.set('page_views', 0)
cache.incr('page_views')  # +1
cache.decr('page_views')  # -1
views = cache.get('page_views')  # Get current value

# -------- EXISTS CHECK (5% of usage) --------
if cache.get('user:1:name'):
    # Key exists
    pass

# -------- CLEAR ALL (Rare, Use Carefully!) --------
cache.clear()  # ⚠️ Only in development!
```

================================================================================
2. WHEN TO USE WHAT (Project Scenarios)
================================================================================

## 🎯 SCENARIO 1: Basic Web Application (90% of projects)

### You Build: E-commerce, Blog, Portfolio, Company Website

```python
# WHAT TO USE: Basic Caching Only

# Use Case 1: Cache database queries
def get_products():
    products = cache.get('all_products')
    if products is None:
        products = Product.objects.filter(is_active=True)
        cache.set('all_products', products, 3600)  # 1 hour
    return products

# Use Case 2: Cache API responses
def get_weather_data(city):
    cache_key = f'weather:{city}'
    weather = cache.get(cache_key)
    if weather is None:
        weather = call_external_api(city)
        cache.set(cache_key, weather, 1800)  # 30 minutes
    return weather

# Use Case 3: Cache template fragments
# In template:
{% cache 3600 product_list products %}
    <!-- Expensive HTML rendering -->
{% endcache %}

# Use Case 4: Store user sessions
# Already handled by Django's session engine
# Just configure:
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
```

### When to Use:
- ✅ Query results that don't change often
- ✅ External API responses
- ✅ Expensive calculations
- ✅ User sessions
- ✅ Static data (navigation menus, categories)

### When NOT to Use:
- ❌ User-specific data (unless you use user ID in key)
- ❌ Frequently changing data (live stock, prices)
- ❌ Large datasets (> 1MB)

---

## 🎯 SCENARIO 2: API Service / Backend

### You Build: REST API for Mobile App, Backend Service

```python
# WHAT TO USE: Caching + Rate Limiting

# Use Case 1: Rate Limiting (Essential for APIs)
from django_redis import get_redis_connection

def check_rate_limit(request):
    redis = get_redis_connection("default")
    user_key = f"rate:{request.user.id}" if request.user.is_authenticated else f"rate:{request.META.get('REMOTE_ADDR')}"
    
    count = redis.get(user_key)
    if count is None:
        redis.set(user_key, 1, ex=60)  # 1 minute
        return True
    elif int(count) >= 100:  # 100 requests per minute
        return False
    else:
        redis.incr(user_key)
        return True

# In views.py
class ProductView(APIView):
    def get(self, request):
        if not check_rate_limit(request):
            return Response({"error": "Rate limit exceeded"}, status=429)
        # ... rest of view

# Use Case 2: Cache API responses
def get_product_list(request):
    page = request.GET.get('page', 1)
    cache_key = f'api:products:page:{page}'
    
    response = cache.get(cache_key)
    if response is None:
        products = Product.objects.all()[page*10:page*10+10]
        serializer = ProductSerializer(products, many=True)
        response = serializer.data
        cache.set(cache_key, response, 300)  # 5 minutes
    return Response(response)
```

---

## 🎯 SCENARIO 3: Assessment / Exam Platform

### You Build: Quiz App, Exam System, Assessment Platform

```python
# WHAT TO USE: Caching + Lists + Hashes

# Use Case 1: Cache questions (Read-heavy)
def get_exam_questions(exam_id):
    cache_key = f'exam:{exam_id}:questions'
    questions = cache.get(cache_key)
    if questions is None:
        questions = Question.objects.filter(exam_id=exam_id, is_active=True)
        cache.set(cache_key, questions, 86400)  # 24 hours
    return questions

# Use Case 2: Store user answers temporarily (Hash)
from django_redis import get_redis_connection
redis = get_redis_connection("default")

def save_user_answer(user_id, question_id, answer):
    key = f'exam:user:{user_id}:answers'
    redis.hset(key, question_id, answer)
    redis.expire(key, 7200)  # 2 hours

def get_user_answers(user_id):
    key = f'exam:user:{user_id}:answers'
    return redis.hgetall(key)

# Use Case 3: Track active users (Set)
def mark_user_active(user_id, exam_id):
    key = f'exam:{exam_id}:active_users'
    redis.sadd(key, user_id)
    redis.expire(key, 3600)  # 1 hour

def get_active_users(exam_id):
    key = f'exam:{exam_id}:active_users'
    return redis.smembers(key)

# Use Case 4: Simple queue for auto-scoring (List)
def queue_for_scoring(submission_id):
    redis.lpush('scoring:queue', submission_id)

# Celery will process this queue
```

---

## 🎯 SCENARIO 4: Social Media / Real-Time App

### You Build: Social Network, Chat App, Activity Feed

```python
# WHAT TO USE: Caching + Lists + Sets + Sorted Sets

# Use Case 1: Recent activities (List)
def add_activity(user_id, activity):
    key = f'user:{user_id}:activities'
    redis.lpush(key, activity)
    redis.ltrim(key, 0, 99)  # Keep last 100
    redis.expire(key, 604800)  # 7 days

def get_recent_activities(user_id, count=10):
    key = f'user:{user_id}:activities'
    return redis.lrange(key, 0, count-1)

# Use Case 2: Following/Followers (Set)
def follow_user(user_id, follow_id):
    redis.sadd(f'user:{user_id}:following', follow_id)
    redis.sadd(f'user:{follow_id}:followers', user_id)

def unfollow_user(user_id, follow_id):
    redis.srem(f'user:{user_id}:following', follow_id)
    redis.srem(f'user:{follow_id}:followers', user_id)

def get_followers(user_id):
    return redis.smembers(f'user:{user_id}:followers')

# Use Case 3: Leaderboard (Sorted Set)
def update_score(user_id, points):
    redis.zadd('leaderboard:global', {user_id: points})

def get_top_players(limit=10):
    return redis.zrevrange('leaderboard:global', 0, limit-1, withscores=True)

def get_user_rank(user_id):
    return redis.zrevrank('leaderboard:global', user_id)

# Use Case 4: Track online users (Set)
def user_online(user_id):
    redis.sadd('online_users', user_id)
    redis.expire('online_users', 300)  # Auto-cleanup

def user_offline(user_id):
    redis.srem('online_users', user_id)

def get_online_users():
    return redis.smembers('online_users')
```

---

## 🎯 SCENARIO 5: E-commerce Platform

### You Build: Shopping Cart, Product Catalog, Order System

```python
# WHAT TO USE: Caching + Hashes + Lists

# Use Case 1: Shopping Cart (Hash)
def add_to_cart(user_id, product_id, quantity):
    key = f'cart:{user_id}'
    redis.hset(key, f'product:{product_id}', quantity)
    redis.expire(key, 86400)  # 24 hours

def get_cart(user_id):
    key = f'cart:{user_id}'
    return redis.hgetall(key)

def remove_from_cart(user_id, product_id):
    key = f'cart:{user_id}'
    redis.hdel(key, f'product:{product_id}')

# Use Case 2: Product View Counts
def increment_views(product_id):
    redis.incr(f'product:{product_id}:views')

def get_views(product_id):
    return redis.get(f'product:{product_id}:views') or 0

# Use Case 3: Recently Viewed Products (List)
def add_recently_viewed(user_id, product_id):
    key = f'user:{user_id}:recent_products'
    redis.lrem(key, 0, product_id)  # Remove if exists
    redis.lpush(key, product_id)
    redis.ltrim(key, 0, 9)  # Keep last 10
    redis.expire(key, 604800)  # 7 days

def get_recently_viewed(user_id):
    key = f'user:{user_id}:recent_products'
    return redis.lrange(key, 0, -1)

# Use Case 4: Inventory Tracking
def check_stock(product_id):
    stock = cache.get(f'product:{product_id}:stock')
    if stock is None:
        stock = Product.objects.get(id=product_id).stock
        cache.set(f'product:{product_id}:stock', stock, 60)
    return stock

def update_stock(product_id, quantity):
    product = Product.objects.get(id=product_id)
    product.stock -= quantity
    product.save()
    cache.set(f'product:{product_id}:stock', product.stock, 60)
```

================================================================================
3. STEP-BY-STEP IMPLEMENTATION GUIDE
================================================================================

## 🚀 STEP 1: Setup for First Project (15 minutes)

```bash
# 1. Install packages
pip install django-redis redis hiredis

# 2. Install Redis
# On macOS:
brew install redis
brew services start redis

# On Ubuntu:
sudo apt-get install redis-server
sudo systemctl start redis

# 3. Add to settings.py
```

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'myapp',
    }
}

# 4. Test in Django shell
# python manage.py shell
from django.core.cache import cache
cache.set('test', 'Hello Redis', 60)
print(cache.get('test'))  # Should print: Hello Redis
```

## 🚀 STEP 2: Add Caching to Your Views (30 minutes)

### Example: Product List

```python
# BEFORE (Without Cache)
from django.shortcuts import render
from .models import Product

def product_list(request):
    products = Product.objects.all().select_related('category')
    return render(request, 'products/list.html', {'products': products})

# AFTER (With Cache)
from django.core.cache import cache
from django.shortcuts import render
from .models import Product

def product_list(request):
    # Get page number from request
    page = request.GET.get('page', 1)
    cache_key = f'products:list:page:{page}'
    
    # Try to get from cache
    products = cache.get(cache_key)
    if products is None:
        # Cache miss - query database
        products = Product.objects.all().select_related('category')
        # Cache for 1 hour
        cache.set(cache_key, products, 3600)
    
    return render(request, 'products/list.html', {'products': products})
```

### Example: API Endpoint

```python
# BEFORE (Without Cache)
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# AFTER (With Cache)
from django.core.cache import cache
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def list(self, request):
        cache_key = 'products:list'
        
        # Try cache
        data = cache.get(cache_key)
        if data is None:
            # Cache miss
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            cache.set(cache_key, data, 3600)  # 1 hour
        
        return Response(data)
    
    def create(self, request, *args, **kwargs):
        # Clear cache when creating
        cache.delete('products:list')
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        # Clear cache when updating
        cache.delete('products:list')
        return super().update(request, *args, **kwargs)
```

## 🚀 STEP 3: Add Rate Limiting (1 hour)

### Create a Rate Limiter Middleware

```python
# middleware/rate_limit.py
from django_redis import get_redis_connection
from django.http import JsonResponse
import re

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Define rate limits for different endpoints
        self.rate_limits = {
            'login': {'requests': 10, 'time': 60},  # 10 per minute
            'api': {'requests': 100, 'time': 60},   # 100 per minute
            'register': {'requests': 5, 'time': 3600},  # 5 per hour
        }
    
    def __call__(self, request):
        # Determine which rate limit to apply
        path = request.path
        limit_type = None
        
        if '/login/' in path:
            limit_type = 'login'
        elif '/api/' in path:
            limit_type = 'api'
        elif '/register/' in path:
            limit_type = 'register'
        
        if limit_type:
            if not self.check_rate_limit(request, limit_type):
                return JsonResponse({
                    'error': 'Rate limit exceeded. Please try again later.'
                }, status=429)
        
        return self.get_response(request)
    
    def check_rate_limit(self, request, limit_type):
        # Get user identifier
        if request.user.is_authenticated:
            user_id = request.user.id
        else:
            user_id = request.META.get('REMOTE_ADDR', 'unknown')
        
        # Get rate limit config
        config = self.rate_limits[limit_type]
        key = f'rate_limit:{limit_type}:{user_id}'
        
        redis_conn = get_redis_connection("default")
        
        # Get current count
        count = redis_conn.get(key)
        
        if count is None:
            # First request
            redis_conn.set(key, 1, ex=config['time'])
            return True
        
        count = int(count)
        if count >= config['requests']:
            return False
        
        # Increment count
        redis_conn.incr(key)
        return True
```

### Add to settings.py

```python
# settings.py
MIDDLEWARE = [
    # ... other middleware
    'middleware.rate_limit.RateLimitMiddleware',  # Add this
]
```

## 🚀 STEP 4: Implement Cache Invalidation (1 hour)

### Different Strategies

```python
# Strategy 1: Delete on Update (Simplest)
from django.core.cache import cache

def update_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.title = request.POST['title']
    product.save()
    
    # Delete individual product cache
    cache.delete(f'product:{product_id}')
    # Delete list cache
    cache.delete('products:list')
    return redirect('product_detail', product_id=product_id)


# Strategy 2: Version-Based Caching (More Robust)
def get_product_list(request):
    # Get current version
    version = cache.get('products:version', 1)
    cache_key = f'products:list:v{version}'
    
    data = cache.get(cache_key)
    if data is None:
        data = Product.objects.all()
        cache.set(cache_key, data, 3600)
    return data

def update_product(request, product_id):
    # Update database
    product = Product.objects.get(id=product_id)
    product.title = request.POST['title']
    product.save()
    
    # Increment version to invalidate all caches
    cache.incr('products:version')
    return redirect('product_detail', product_id=product_id)


# Strategy 3: Tag-Based Caching (With django-cache-tag)
from cache_tag import cache_tag

@cache_tag('products')
def get_products():
    return Product.objects.all()

def update_product(request, product_id):
    # ... update product
    # Invalidate all caches with 'products' tag
    cache_tag.invalidate('products')
```

================================================================================
4. COMMON PATTERNS & BEST PRACTICES
================================================================================

## ✅ DO's

### 1. Use Meaningful Key Names
```python
# ✅ GOOD - Clear and organized
cache_key = f'user:{user_id}:profile:settings'
cache_key = f'product:{product_id}:reviews:page:{page}'

# ❌ BAD - Confusing
cache_key = f'u{user_id}ps'
cache_key = 'data123'
```

### 2. Always Set TTL (Time To Live)
```python
# ✅ GOOD
cache.set(key, value, timeout=3600)  # 1 hour
cache.set(key, value, timeout=300)   # 5 minutes

# ❌ BAD - Never expires
cache.set(key, value)
```

### 3. Use Lazy Loading Pattern
```python
# ✅ GOOD - Standard pattern
def get_cached_data(key):
    data = cache.get(key)
    if data is None:
        data = expensive_operation()
        cache.set(key, data, 3600)
    return data

# ❌ BAD - Inconsistent
data = cache.get(key)
if not data:
    data = expensive_operation()
    cache.set(key, data)
```

### 4. Handle Cache Misses Gracefully
```python
# ✅ GOOD
data = cache.get(key)
if data is None:
    try:
        data = database_query()
        cache.set(key, data, 3600)
    except DatabaseError:
        # Fallback to default value
        data = default_value

# ❌ BAD - No error handling
data = cache.get(key)
if data is None:
    data = database_query()  # Could fail here
    cache.set(key, data, 3600)
```

### 5. Cache Expensive Operations
```python
# ✅ GOOD - Expensive operations
data = cache.get(key)
if data is None:
    # Complex joins, aggregations, or calculations
    data = Model.objects.annotate(complex_calculation()).filter(...)
    cache.set(key, data, 3600)

# ❌ BAD - Caching simple operations
# Don't cache simple operations
data = Model.objects.get(id=1)  # Fast query, no cache needed
```

## ❌ DON'Ts

### 1. Don't Cache User-Specific Data Globally
```python
# ❌ BAD - User data in global cache
cache.set('user_data', user_data)  # Overwrites for all users

# ✅ GOOD - Include user ID in key
cache.set(f'user:{user_id}:data', user_data)
```

### 2. Don't Store Large Objects
```python
# ❌ BAD - Storing large objects
images = Product.objects.filter(...)  # Many images
cache.set('products', images)  # Could be > 1MB

# ✅ GOOD - Cache only what you need
data = Product.objects.values('id', 'name', 'price')  # Only needed fields
cache.set('products', list(data), 3600)
```

### 3. Don't Forget to Invalidate
```python
# ❌ BAD - Never invalidates
def update_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.save()
    return Response({'status': 'updated'})  # Cache still has old data

# ✅ GOOD - Invalidates cache
def update_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.save()
    cache.delete(f'product:{product_id}')  # Clear this product cache
    cache.delete('products:list')  # Clear the list cache
    return Response({'status': 'updated'})
```

### 4. Don't Use Redis for Everything
```python
# ❌ BAD - Using Redis for everything
# Redis doesn't have complex queries like Django ORM
cache.set('all_products', Product.objects.all())  # No filtering

# ✅ GOOD - Use PostgreSQL for complex queries
products = Product.objects.filter(
    category=category, 
    price__lt=100
).order_by('name')
# This query is better in PostgreSQL
```

### 5. Don't Create Too Many Keys
```python
# ❌ BAD - Creating keys for every request
cache.set(f'page:{request.path}:{timezone.now()}', data)  # Unique per second

# ✅ GOOD - Use fixed keys
cache.set(f'page:{request.path}', data, 3600)  # Same key, just expires
```

================================================================================
5. PROJECT SCENARIOS QUICK REFERENCE
================================================================================

## 🏗️ PROJECT TYPE: Simple Blog/Website
### Use:
```python
# 1. Cache rendered HTML
cache.set('homepage', rendered_html, 600)  # 10 minutes

# 2. Cache database queries
cache.set('categories', Category.objects.all(), 3600)

# 3. Cache popular posts
cache.set('popular_posts', popular_posts, 300)
```

## 🏗️ PROJECT TYPE: E-commerce
### Use:
```python
# 1. Cache product list
cache.set('products:page:1', products, 300)

# 2. Cache shopping cart (Hash)
redis.hset(f'cart:{user_id}', product_id, quantity)

# 3. Track product views
cache.incr(f'product:{product_id}:views')

# 4. Cache inventory
cache.set(f'product:{product_id}:stock', stock, 60)
```

## 🏗️ PROJECT TYPE: API Service
### Use:
```python
# 1. Rate limiting (most important!)
rate_limit = redis.get(f'rate:{ip}')

# 2. Cache API responses
cache.set(f'api:users:list', response_data, 300)

# 3. Cache JWT token blacklist
cache.set(f'token:blacklist:{token}', True, 86400)
```

## 🏗️ PROJECT TYPE: Assessment/Quiz Platform
### Use:
```python
# 1. Cache questions
cache.set(f'exam:{exam_id}:questions', questions, 86400)

# 2. Store temporary answers (Hash)
redis.hset(f'exam:{user_id}:answers', question_id, answer)

# 3. Track active users (Set)
redis.sadd(f'exam:{exam_id}:active_users', user_id)

# 4. Queue for grading (List)
redis.lpush('grading:queue', submission_id)
```

## 🏗️ PROJECT TYPE: Social Media
### Use:
```python
# 1. Activity feed (List)
redis.lpush(f'user:{user_id}:feed', activity)

# 2. Follower system (Set)
redis.sadd(f'user:{user_id}:followers', follower_id)

# 3. Leaderboard (Sorted Set)
redis.zadd('leaderboard', {user_id: points})

# 4. Online users (Set)
redis.sadd('online_users', user_id)
```

================================================================================
6. TROUBLESHOOTING CHECKLIST
================================================================================

## 🐛 Redis Not Working?

### 1. Check if Redis is running
```bash
# Check process
ps aux | grep redis

# Check service
sudo systemctl status redis

# Try to connect
redis-cli ping  # Should return PONG
```

### 2. Check Connection Settings
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',  # Is this correct?
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    }
}
```

### 3. Check Redis Memory
```bash
# Check memory usage
redis-cli info memory

# Check max memory
redis-cli config get maxmemory
```

### 4. Clear Redis (Development Only)
```bash
# Clear all databases
redis-cli flushall

# Clear specific database
redis-cli -n 1 flushdb
```

### 5. Check Django Settings
```python
# In Django shell
from django.core.cache import cache
cache.set('test', 'value', 10)
cache.get('test')  # Should return 'value'
```

================================================================================
7. QUICK REFERENCE CHEATSHEET
================================================================================

## 🚀 Django Core Cache
```python
from django.core.cache import cache

# Set
cache.set(key, value, timeout=3600)

# Get
value = cache.get(key)
value = cache.get(key, default_value)

# Delete
cache.delete(key)

# Increment
cache.incr(key)
cache.decr(key)

# Check exists
if cache.get(key) is not None:
    pass

# Clear all (development only)
cache.clear()
```

## 🔴 Redis Direct Operations
```python
from django_redis import get_redis_connection
redis = get_redis_connection("default")

# STRINGS
redis.set(key, value, ex=3600)
value = redis.get(key)
redis.incr(key)
redis.decr(key)
redis.delete(key)

# LISTS
redis.lpush(key, value)
redis.rpush(key, value)
value = redis.lpop(key)
value = redis.rpop(key)
values = redis.lrange(key, 0, -1)
redis.llen(key)

# HASHES
redis.hset(key, field, value)
redis.hmset(key, {field1: value1, field2: value2})
value = redis.hget(key, field)
all = redis.hgetall(key)
redis.hdel(key, field)
redis.hexists(key, field)

# SETS
redis.sadd(key, value1, value2)
redis.srem(key, value)
values = redis.smembers(key)
is_member = redis.sismember(key, value)
count = redis.scard(key)

# SORTED SETS
redis.zadd(key, {member: score})
redis.zrem(key, member)
ranking = redis.zrevrank(key, member)
top = redis.zrevrange(key, 0, 9, withscores=True)
```

## 📋 Common Key Patterns
```python
# User related
f'user:{user_id}:profile'
f'user:{user_id}:settings'
f'user:{user_id}:cart'

# Product related
f'product:{product_id}'
f'product:{product_id}:reviews'
f'products:list:page:{page}'

# API related
f'api:{endpoint_name}:version:{version}'
f'api:{endpoint_name}:params:{hash}'

# Rate limiting
f'rate:{endpoint}:{user_id}'
f'rate:{endpoint}:{ip_address}'

# Session
f'session:{session_key}'

# Temporary data
f'temp:{user_id}:{action}:{timestamp}'
```

================================================================================
8. WHAT TO LEARN NEXT (Progression Path)
================================================================================

## 📚 Junior Developer → Mid-Level
```python
# Learn these next (in order):

# 1. Cache Invalidation Patterns
# - When to delete vs update
# - Version-based invalidation
# - Cache tags

# 2. Redis Lists for Queues
# - Simple task queues
# - Recent items
# - Activity feeds

# 3. Redis Hashes
# - Storing user profiles
# - Temporary data storage

# 4. Rate Limiting
# - Different limit types
# - Per-user vs IP-based

# 5. Redis with Celery
# - Setting up Celery with Redis
# - Background tasks
```

## 📚 Mid-Level Developer → Senior
```python
# Learn these for advanced projects:

# 1. Sorted Sets
# - Leaderboards
# - Real-time rankings
# - Priority queues

# 2. Redis Pub/Sub
# - Real-time notifications
# - WebSocket integration

# 3. Redis Transactions
# - Lua scripts
# - Atomic operations

# 4. Redis with Docker
# - Containerization
# - Scaling Redis

# 5. Redis Monitoring
# - Performance tuning
# - Memory optimization
```

================================================================================
9. SUMMARY: WHAT A JUNIOR DEVELOPS SHOULD KNOW
================================================================================

## ✅ Must Know (90% of daily work)
1. How to configure Django with Redis
2. `cache.set()`, `cache.get()`, `cache.delete()`
3. Setting TTL/timeout
4. Cache invalidation basics
5. When to use Redis (cache expensive queries)

## ✅ Should Know (8% of daily work)
1. Redis Lists for simple queues
2. Redis Hashes for structured data
3. Redis Sets for unique tracking
4. Rate limiting with Redis

## ✅ Nice to Know (2% of daily work)
1. Sorted Sets for leaderboards
2. Redis Pub/Sub for real-time features
3. Advanced cache patterns

## ❌ Don't Need to Know (Unless Required)
1. Redis Cluster (DevOps handles)
2. Redis Replication (DevOps handles)
3. Redis Sentinel (DevOps handles)
4. Lua Scripting (Use Python instead)
5. Redis Streams (Use Celery instead)

================================================================================
END OF DOCUMENT
================================================================================