# CombatAtlas - Martial Arts Drills Database

## Overview
CombatAtlas is a Django REST Framework application designed to serve as a comprehensive database for martial arts drills. The application organizes martial arts content into a hierarchical structure: Martial Arts -> Categories -> Drill Exercises.

## Project Structure
- **combatAtlas_Backend**: Django backend application
  - **combatAtlas_Backend**: Main Django project configuration
  - **core**: Django app containing models, views, and serializers
- **combatAtlas_Frontend**: Frontend application (currently empty)

## Core Models

### MartialArt
- `name`: CharField (max_length=100, unique=True)
- `sport_type`: TextField
- `description`: TextField
- `image`: ImageField (optional)
- `created_at`: DateTimeField (auto_now_add)

### DrillCategory
- `name`: CharField (max_length=100)
- `martial_art`: ForeignKey to MartialArt
- `description`: TextField
- `image`: ImageField (optional)
- `created_at`: DateTimeField (auto_now_add)

### DrillExercise
- `name`: CharField (max_length=100)
- `difficulty_level`: CharField (max_length=50)
- `drill_type`: CharField (max_length=100)
- `category`: ForeignKey to DrillCategory
- `description`: TextField
- `image`: ImageField (optional)
- `video_url`: URLField (optional)
- `created_at`: DateTimeField (auto_now_add)

## API Endpoints
Based on the views.py file, the following API endpoints are implemented:

### MartialArtViewSet
- Standard CRUD operations for MartialArt
- Custom action: `categories` (GET /martial-arts/{id}/categories/) - returns categories for a specific martial art

### DrillCategoryViewSet
- Standard CRUD operations for DrillCategory
- Custom action: `drills` (GET /drill-categories/{id}/drills/) - returns drills for a specific category

### DrillExerciseViewSet
- Standard CRUD operations for DrillExercise
- Custom action: `random` (GET /drill-exercises/random/) - returns a random drill exercise with optional filtering by martial_art and category query parameters

### UserViewSet & GroupViewSet
- Standard CRUD operations for Django Users and Groups (requires authentication)

## Permissions
- Most endpoints use `IsAuthenticatedOrReadOnly` allowing read access to unauthenticated users
- User and Group endpoints require authentication (`IsAuthenticated`)

## Setup Requirements
Based on the project structure, this appears to be a Django project requiring:
- Python 3.x
- Django
- Django REST Framework
- Pillow (for ImageField handling)
- A database (SQLite is configured by default)

## Next Steps for Completion
1. **Frontend Development**: The combatAtlas_Frontend directory is currently empty and needs to be developed
2. **API Testing**: Test the existing API endpoints to ensure they work correctly
3. **Data Population**: Add initial martial arts, categories, and drills to make the application useful
4. **Deployment Preparation**: 
   - Configure production settings
   - Set up proper static/media file handling
   - Configure allowed hosts and security settings
5. **Documentation**: Create API documentation (Swagger/OpenAPI)
6. **User Interface**: Build a frontend to interact with the API (could be React, Vue, or Django templates)

## Current State
The backend appears to be functional with:
- Properly defined models with relationships
- Serializers (imported but not shown in the snippet)
- ViewSets with custom actions
- Basic permissions configured
- A pre-populated SQLite database (db.sqlite3)

The frontend directory exists but contains no files, indicating frontend work has not yet begun.

## Integration Opportunities
This project could integrate with:
- The coding school platform for teaching martial arts concepts
- Local meeting transcriber for recording and analyzing martial arts training sessions
- Music mood app for creating training playlists
- Sleep/dream app for tracking recovery and performance