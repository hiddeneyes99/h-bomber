# Overview

This is a Telegram bot application that provides call and SMS bombing functionality through multiple API integrations. The bot includes an admin panel for managing users, protected numbers, credits, and access control. It uses SQLite for data persistence and implements features like credit systems, redeem codes, broadcasting, and number protection mechanisms.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Bot Framework
- **Primary Framework**: python-telegram-bot (v20.7)
- **Rationale**: Modern async-first Telegram bot library with comprehensive API coverage
- **Architecture Pattern**: Handler-based event processing with CommandHandler, MessageHandler, and CallbackQueryHandler
- **Async Processing**: Built on asyncio for non-blocking API calls and concurrent request handling

## Data Storage
- **Database**: SQLite3
- **Rationale**: Lightweight, serverless database suitable for managing user data, credits, protected numbers, banned users, and redeem codes
- **Schema Components**:
  - User management (registrations, credits, access control)
  - Protected numbers registry
  - Banned users tracking
  - Redeem codes and redemption history
  - Credit transaction logs

## API Integration Layer
- **HTTP Client**: aiohttp for asynchronous API requests
- **API Pool**: Large collection (3000+) of third-party APIs for call/SMS delivery
- **Request Strategy**: Concurrent bombing across multiple endpoints
- **APIs Categories**:
  - Voice call APIs (Tata Capital, 1MG, Swiggy, Myntra, Flipkart, etc.)
  - SMS APIs
  - OTP verification services
- **Pros**: Distributed approach prevents single point of failure; high success rate
- **Cons**: Depends on third-party API availability; requires maintenance as APIs change

## Security & Access Control
- **Admin System**: Decorator-based admin authentication
- **Access Layers**:
  - Number protection system (prevents bombing protected numbers)
  - User ban/unban functionality
  - Whitelist/allowlist system
  - Credit-based rate limiting
- **Rationale**: Multi-layered protection prevents abuse and allows granular control

## Credit System
- **Economy Model**: Credit-based usage tracking
- **Features**:
  - Per-user credit balance
  - Credit allocation by admin
  - Redeem code generation and validation
  - Credit deduction per bombing operation
- **Rationale**: Prevents spam and unlimited abuse while allowing controlled access

## Admin Panel
- **Interface**: Custom keyboard-based menu system
- **Capabilities**:
  - Number protection management
  - User access control (ban/unban/allow/disallow)
  - Credit management and allocation
  - Redeem code generation
  - Broadcasting to all users
  - List viewing (users, banned, protected, codes)
- **Design Pattern**: Command pattern with state management

## UI Components
- **Keyboard Types**: 
  - ReplyKeyboardMarkup for persistent menus
  - InlineKeyboardMarkup for contextual actions
  - KeyboardButton for user input collection
- **Visual Feedback**: Colorama for terminal logging with color-coded output
- **Rationale**: Provides intuitive navigation and clear visual hierarchy

## Configuration Management
- **Environment Variables**: python-dotenv for secure credential storage
- **Expected Variables**: Telegram bot token, admin IDs, API keys
- **Rationale**: Separates configuration from code; enhances security

# External Dependencies

## Core Libraries
- **python-telegram-bot (v20.7)**: Official Telegram Bot API wrapper for Python
- **aiohttp**: Asynchronous HTTP client for API requests
- **colorama**: Cross-platform colored terminal text for logging
- **python-dotenv**: Environment variable management from .env files

## Built-in Libraries
- **sqlite3**: Database operations (Python standard library)
- **asyncio**: Asynchronous I/O and concurrency (Python standard library)
- **datetime**: Date/time handling for credits, bans, and logging
- **json**: API request/response serialization
- **threading**: Parallel task execution
- **random**: Randomization for API selection and delays
- **time**: Rate limiting and timing operations

## Third-Party Services
- **Telegram Bot API**: Primary platform for bot operation
- **Call/SMS APIs**: 3000+ endpoints including:
  - Tata Capital (voice OTP)
  - 1MG (voice OTP)
  - Swiggy (call verification)
  - Myntra (voice OTP)
  - Flipkart (voice OTP)
  - Various other Indian service providers
- **Characteristics**: No authentication required for most APIs; publicly accessible endpoints

## Database Schema (SQLite)
- **Tables** (inferred):
  - users: User registration and credit tracking
  - protected_numbers: Numbers excluded from bombing
  - banned_users: Blocked user IDs
  - allowed_users: Whitelisted users
  - redeem_codes: Generated codes with credit values
  - credit_logs: Transaction history