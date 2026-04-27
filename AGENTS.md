# Project instructions

This is a diploma project: an information system for a coffee shop.

## Main goal

Build a web-based information system for a coffee shop with:
- user registration and authentication;
- user profile;
- loyalty card with bonuses;
- menu;
- pre-order system;
- order history;
- referral program;
- promotions;
- coffee shop location page;
- admin panel.

## Technology stack

Backend:
- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- JWT authentication

Frontend:
- React or simple HTML/CSS/JS
- Responsive design

Infrastructure:
- Docker
- docker-compose
- .env configuration

## Coding rules

- Keep code clean and modular.
- Do not put business logic directly inside routers.
- Use layered architecture:
  Router -> Service -> Repository -> Database.
- Use English names for code, variables, functions, classes and files.
- Comments may be in Russian.
- Add validation with Pydantic schemas.
- Add error handling.
- Use meaningful names.
- Do not create unnecessary complexity.
- The project should be understandable for diploma defense.

## Backend modules

Required backend modules:
- auth
- users
- menu
- orders
- loyalty
- referrals
- promotions
- admin

Each module should contain:
- router.py
- schemas.py
- models.py
- service.py
- repository.py

## Database requirements

Use PostgreSQL.

Main entities:
- users
- profiles
- roles
- categories
- products
- orders
- order_items
- loyalty_cards
- bonus_transactions
- referrals
- promotions
- coffee_shops

## Business rules

Loyalty:
- each user has a loyalty card;
- bonuses are accrued after completed orders;
- bonuses can be used to partially pay for orders;
- all bonus accruals and write-offs must be stored in bonus_transactions.

Orders:
- order statuses: created, accepted, preparing, ready, completed, cancelled;
- there are two order types: offline and preorder.

Referral program:
- each user has a referral code;
- invited user can apply referral code once;
- referral bonuses are given after the invited user's first completed order.

## Important

Before making big changes:
- inspect the existing structure;
- follow current architecture;
- do not rewrite the whole project unnecessarily;
- explain what files were changed.