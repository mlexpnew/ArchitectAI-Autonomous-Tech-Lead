PROMPTS = {

    "model":
"""
Generate ONLY a SQLAlchemy model.

Requirements:

- SQLAlchemy 2.0
- Type hints
- Python only
- No markdown
- No explanation

Entity:
{entity}
""",

    "schema":
"""
Generate ONLY Pydantic schemas.

Requirements:

- Base
- Create
- Update
- Response

Entity:
{entity}
""",

    "repository":
"""
Generate ONLY Repository class.

Requirements:

CRUD methods

Entity:
{entity}
""",

    "service":
"""
Generate ONLY Service class.

Entity:
{entity}
""",

    "api":
"""
Generate ONLY FastAPI Router.

Entity:
{entity}
"""
}