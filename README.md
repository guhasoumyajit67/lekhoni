# 📝 Lekhoni - Poetry Writing & Sharing Platform

A modern, multi-user poetry writing and sharing platform built with Django. Write, share, and discover beautiful poems in Bengali and English.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0-green.svg)](https://www.djangoproject.com/)
[![Render](https://img.shields.io/badge/Deployed%20on-Render-purple.svg)](https://render.com)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)]()

## 🌐 Live Demo

**View the live application:** [https://lekhoni-by2b.onrender.com](https://lekhoni-by2b.onrender.com)

---

## 📖 Table of Contents
- [🎥 Demo Video](#-demo-video)
- [📸 Screenshots](#-screenshots)
- [✨ Features](#-features)
- [🤔 Why Lekhoni?](#-why-lekhoni)
- [🛠️ Tech Stack](#️-tech-stack)
- [🚀 Quick Start](#-quick-start)
- [🏗️ Project Structure](#️-project-structure)
- [📦 Data Models](#-data-models)
- [🛠️ Management Commands](#️-management-commands)
- [🔧 Configuration](#-configuration)
- [🚀 Deployment](#-deployment)
- [📊 URL Structure](#-url-structure)
- [🧪 Testing](#-testing)
- [📈 Key Technical Decisions](#-key-technical-decisions)
- [📧 Contact](#-contact)

---

## 🎥 Demo Video

Watch a quick 2-minute demo of Lekhoni in action:

[![Lekhoni Demo - Poetry Writing Platform](https://img.youtube.com/vi/YOUR_VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

### What's Covered in the Demo:
- 🏠 **Homepage** - Hero section with search bar and category cards
- 🔥 **Popular Poems** - Trending poems from the last 7 days
- 📖 **Poem Detail** - Reading, liking, and commenting on poems
- ✍️ **Create Poem** - Writing and publishing new poems
- 📊 **My Poems Dashboard** - Managing poems with analytics
- 🏷️ **Categories** - Browsing poems by category
- 📱 **Mobile Responsive** - Works perfectly on all devices

---

## 📸 Screenshots

### Homepage
![Homepage](screenshots/homepage.png)
*Hero section with search bar, popular poems, and category cards.*

### All Poems
![All Poems](screenshots/all_poems.png)
*Browse all poems with infinite scroll loading.*

### Poem Details
![Poem Details](screenshots/poem_details.png)
*Read poems, like, comment, and share with others.*

### Create Poem
![Create Poem](screenshots/create_poem.png)
*Write and publish new poems with Bengali form labels.*

### My Poems Dashboard
![My Poems Dashboard](screenshots/my_poems_dashboard.png)
*Manage your poems with analytics and quick edit/delete options.*

### Categories
![Categories](screenshots/categories.png)
*Browse poems by category with infinite scroll.*

### Comment Section
![Comment Section](screenshots/comment_section.png)
*Read and interact with comments on poems.*

### Mobile Responsive
![Mobile Responsive](screenshots/mobile_responsive.png)
*Fully responsive design that works on all devices.*

---

## ✨ Features

### 🎯 Core Functionality
- **User Authentication** - Custom user model with registration, login, password reset, and profile management
- **Poem Management** - Full CRUD operations for poems with slug-based URLs
- **Category System** - 22 predefined categories with Bengali names, slugs, and FontAwesome icons
- **Comment System** - Users can comment on poems with edit/delete capabilities
- **Like System** - Like/unlike poems with real-time AJAX updates

### 📊 Advanced Features
- **Poem of the Day** - Automatically picks the most viewed poem from the last 24 hours
- **Popular Poems** - Shows trending poems from the last 7 days
- **Featured Poem** - Highlight a featured poem on the homepage
- **Infinite Scroll** - Load more poems seamlessly with AJAX
- **Search Functionality** - Search poems by title, content, category, or author
- **My Poems Dashboard** - View and manage your own poems with analytics
- **Category-Based Filtering** - Browse poems by category
- **View Counter** - Track poem popularity with automatic view counting
- **About Page** - Platform statistics (total poems, authors, categories)

### 🎨 Smart UI Features
- **Full Bengali Interface** - Complete Bengali UI with Bengali fonts (Hind Siliguri, Noto Serif Bengali)
- **Bengali Number Formatting** - Convert English numbers to Bengali numerals (১২৩)
- **Bengali Date Format** - Display dates in Bengali format (২৫ জানুয়ারী, ২০২৬)
- **Responsive Design** - Works on all devices
- **Clean Typography** - Beautiful layout for poetry reading
- **AJAX Interactions** - Smooth like, comment, and load-more functionality
- **Custom CSS & JS** - Tailored styling for poetry platform
- **FontAwesome Icons** - Beautiful icons for categories and actions
- **Dark Theme for Poem of the Day** - Elegant dark section for featured content
- **Hero Section** - Engaging landing page with search bar
- **Category Cards** - Visual category browsing with icons and poem counts

### 📊 Analytics
- **Total Poem Count** - Track platform growth
- **Total Authors** - Number of contributing poets
- **Total Categories** - Available categories
- **Poem Views** - Individual poem popularity
- **Author Stats** - Poems written and total views per author

---

## 🤔 Why Lekhoni?

- **Simple** - Easy-to-use interface for writing and sharing poetry
- **Beautiful** - Clean design that puts poetry front and center
- **Bilingual** - Supports both Bengali and English
- **Community** - Build a community of poetry lovers
- **Free** - Open source and self-hosted

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **Django 6.0** | Web framework |
| **PostgreSQL / SQLite** | Database |
| **Gunicorn** | WSGI HTTP Server |
| **WhiteNoise** | Static file serving |
| **python-environs** | Environment variable management |

### Frontend
| Technology | Purpose |
|------------|---------|
| **Bootstrap 5** | UI framework |
| **Hind Siliguri Font** | Bengali UI font |
| **Noto Serif Bengali** | Bengali poetry font |
| **FontAwesome 6** | Icons |
| **Custom CSS** | Poetry-specific styling |
| **JavaScript** | AJAX interactions, infinite scroll |
| **django-widget-tweaks** | Form styling |

### Custom Template Tags
| Tag | Purpose |
|-----|---------|
| `bengali_num` | Convert English numbers to Bengali numerals |
| `bengali_date` | Display dates in Bengali format |

### Deployment
| Technology | Purpose |
|------------|---------|
| **Render** | Cloud hosting |
| **psycopg3** | PostgreSQL adapter |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- PostgreSQL (optional, SQLite works for development)
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/lekhoni.git
cd lekhoni
```

2. **Create and activate a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
# For PostgreSQL: postgres://user:password@localhost:5432/dbname

# Email Configuration (optional for development)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@example.com
```

5. **Run database migrations**
```bash
python manage.py migrate
```

6. **Create default categories**
```bash
python manage.py create_categories
```
This will create 22 predefined categories with Bengali names, slugs, and FontAwesome icons.

7. **Create a superuser (admin)**
```bash
python manage.py createsuperuser
```

8. **Collect static files**
```bash
python manage.py collectstatic
```

9. **Run the development server**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser!

---

## 🏗️ Project Structure

```
lekhoni/
├── accounts/                      # User authentication and profile management
│   ├── models.py                  # CustomUser (extends AbstractUser)
│   ├── views.py                   # SignUp, Profile, ProfileUpdate
│   ├── forms.py                   # CustomUserCreationForm, ProfileUpdateForm
│   ├── urls.py                    # /signup/, /profile/, /profile/update/
│   ├── admin.py                   # CustomUserAdmin with poem count
│   └── tests/                     # Comprehensive test suite
│
├── poems/                         # Core poetry functionality
│   ├── models.py                  # Category, Poem, Comment, Like
│   ├── views.py                   # Full CRUD, search, categories, load-more
│   ├── forms.py                   # PoemForm, CommentForm, CommentEditForm
│   ├── urls.py                    # Complete URL routing
│   ├── admin.py                   # Custom admin with permissions
│   ├── management/                # Management commands
│   │   └── commands/
│   │       └── create_categories.py  # Create 22 default categories
│   ├── templatetags/              # Custom template tags
│   │   └── bengali_numbers.py     # Bengali number and date formatting
│   └── tests/                     # Comprehensive test suite
│
├── project/                       # Django project configuration
│   ├── settings.py                # Main settings with environs
│   └── urls.py                    # Main URL configuration
│
├── templates/                     # HTML templates
│   ├── base.html                  # Base template with navigation and footer
│   ├── home.html                  # Homepage with hero, popular, categories, latest
│   ├── partials/                  # Reusable template components
│   │   ├── _poem_card.html        # Poem card for lists
│   │   └── _my_poem_card.html     # Poem card for my poems
│   ├── poems/                     # Poetry templates
│   │   ├── poem_list.html         # All poems with infinite scroll
│   │   ├── poem_detail.html       # Single poem view
│   │   ├── create_poem.html       # Create poem form
│   │   ├── my_poems.html          # User's poems dashboard
│   │   ├── category_list.html     # All categories
│   │   ├── category_detail.html   # Poems by category
│   │   ├── search.html            # Search results
│   │   ├── about.html             # About page with stats
│   │   ├── confirm_delete.html    # Delete confirmation
│   │   ├── comment_edit.html      # Edit comment
│   │   └── comment_confirm_delete.html
│   └── registration/              # Auth templates
│       ├── login.html
│       ├── signup.html
│       ├── profile.html           # User profile display
│       ├── profile_update.html    # Profile edit form
│       └── password_*.html        # Password reset templates
│
├── static/                        # Static files (CSS, JS)
│   ├── css/
│   │   └── custom.css             # Complete custom styles
│   └── js/
│       ├── home.js                # Homepage functionality
│       ├── main.js                # Global JavaScript
│       ├── poem_list.js           # Infinite scroll
│       ├── poem_detail.js         # Like, comment AJAX
│       ├── my_poems.js            # My poems dashboard
│       ├── category_detail.js     # Category view
│       └── search.js              # Search functionality
│
├── staticfiles/                   # Collected static files (production)
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
├── Procfile                       # Deployment configuration
└── db.sqlite3                    # SQLite database (development)
```

---

## 📦 Data Models

### Category
| Field | Type | Description |
|-------|------|-------------|
| `name` | CharField(100) | Category name (Bengali) |
| `slug` | SlugField | URL-friendly identifier |
| `description` | TextField | Category description |
| `icon` | CharField(50) | FontAwesome icon class |

### Poem
| Field | Type | Description |
|-------|------|-------------|
| `title` | CharField(255) | Poem title |
| `slug` | SlugField | URL-friendly identifier (auto-generated) |
| `content` | TextField | Poem content |
| `author` | ForeignKey | User who wrote the poem |
| `category` | ForeignKey | Category reference |
| `is_published` | BooleanField | Published status (auto=true) |
| `is_featured` | BooleanField | Featured poem (admin) |
| `views` | PositiveIntegerField | View counter |
| `created_at` | DateTimeField | Creation timestamp |
| `updated_at` | DateTimeField | Last update timestamp |
| `published_at` | DateTimeField | Publication date |

### Comment
| Field | Type | Description |
|-------|------|-------------|
| `poem` | ForeignKey | Poem being commented on |
| `author` | ForeignKey | User who wrote the comment |
| `content` | TextField | Comment content |
| `is_approved` | BooleanField | Moderation flag |
| `created_at` | DateTimeField | Creation timestamp |
| `updated_at` | DateTimeField | Last update timestamp |

### Like
| Field | Type | Description |
|-------|------|-------------|
| `poem` | ForeignKey | Poem being liked |
| `user` | ForeignKey | User who liked |
| `created_at` | DateTimeField | Creation timestamp |

---

## 🛠️ Management Commands

### Create Categories
```bash
python manage.py create_categories
```
Creates 22 predefined categories with Bengali names, slugs, and FontAwesome icons:

| # | Category (Bengali) | Slug | Icon |
|---|-------------------|------|------|
| 1 | প্রেম | love | fa-heart |
| 2 | বিষাদ | sad | fa-sad-tear |
| 3 | আনন্দ | happy | fa-smile |
| 4 | একাকিত্ব | lonely | fa-user |
| 5 | আশা | hope | fa-sun |
| 6 | প্রকৃতি | nature | fa-tree |
| 7 | বর্ষা | rain | fa-cloud-rain |
| 8 | বসন্ত | spring | fa-seedling |
| 9 | শরৎ | autumn | fa-leaf |
| 10 | দেশপ্রেম | patriotism | fa-flag |
| 11 | মুক্তিযুদ্ধ | liberation_war | fa-fist-raised |
| 12 | জীবন | life | fa-life-ring |
| 13 | স্বপ্ন | dream | fa-moon |
| 14 | সংগ্রাম | struggle | fa-hand-fist |
| 15 | যাত্রা | journey | fa-road |
| 16 | আধ্যাত্মিক | spiritual | fa-spa |
| 17 | আধুনিক | modern | fa-laptop |
| 18 | নারীবাদ | feminism | fa-venus |
| 19 | প্রতিবাদ | protest | fa-bullhorn |
| 20 | শিশুতোষ | children | fa-child |
| 21 | রসাত্মক | humor | fa-laugh |
| 22 | অন্যান্য | other | fa-ellipsis-h |

---

## 🔧 Configuration

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Required |
| `DEBUG` | Debug mode | False |
| `DATABASE_URL` | Database connection string | sqlite:///db.sqlite3 |
| `ALLOWED_HOSTS` | Comma-separated list of hosts | localhost,127.0.0.1,.onrender.com |
| `CSRF_TRUSTED_ORIGINS` | CSRF trusted origins | https://*.onrender.com |
| `EMAIL_BACKEND` | Email backend | console.EmailBackend |
| `EMAIL_HOST` | SMTP server | - |
| `EMAIL_PORT` | SMTP port | 587 |
| `EMAIL_USE_TLS` | Use TLS | True |
| `EMAIL_HOST_USER` | SMTP username | - |
| `EMAIL_HOST_PASSWORD` | SMTP password | - |
| `DEFAULT_FROM_EMAIL` | Default sender email | noreply@example.com |

---

## 🚀 Deployment

### Deployed on Render

This application is **live on Render** at: [https://lekhoni-by2b.onrender.com](https://lekhoni-by2b.onrender.com)

The project includes a `Procfile` for easy deployment:

```yaml
web: gunicorn project.wsgi:application --log-file -
```

### Deploy Your Own Instance on Render

1. Push your code to GitHub
2. Create a new Web Service on Render
3. Connect your repository
4. Set environment variables in Render dashboard:
   - `SECRET_KEY` - Your Django secret key
   - `DEBUG` - Set to `False` for production
   - `DATABASE_URL` - Your PostgreSQL database URL
   - `EMAIL_HOST_PASSWORD` - Your email password (if using email)
5. Deploy!

---

## 📊 URL Structure

### Authentication
| URL | View | Description |
|-----|------|-------------|
| `/accounts/signup/` | SignUpView | User registration |
| `/accounts/profile/` | ProfileView | User profile |
| `/accounts/profile/update/` | ProfileUpdateView | Edit profile |
| `/accounts/login/` | - | Login (Django built-in) |
| `/accounts/logout/` | - | Logout (Django built-in) |

### Poems
| URL | View | Description |
|-----|------|-------------|
| `/` | HomeView | Homepage with featured content |
| `/poems/` | PoemListView | All poems with infinite scroll |
| `/poems/load-more/` | LoadMorePoemsView | AJAX load more |
| `/poem/<slug>/` | PoemDetailView | Single poem view |
| `/create/` | CreatePoemView | Create new poem |
| `/update/<slug>/` | UpdatePoemView | Edit poem |
| `/delete/<slug>/` | DeletePoemView | Delete poem |
| `/my-poems/` | MyPoemsView | User's poems dashboard |
| `/my-poems/load-more/` | MyPoemsLoadMoreView | AJAX load more (my poems) |

### Categories
| URL | View | Description |
|-----|------|-------------|
| `/categories/` | CategoryListView | All categories |
| `/category/<slug>/` | CategoryDetailView | Poems by category |
| `/category/<slug>/load-more/` | CategoryLoadMorePoemsView | AJAX load more |

### Interactions
| URL | View | Description |
|-----|------|-------------|
| `/like/<slug>/` | ToggleLikeView | Like/unlike poem (AJAX) |
| `/comment/edit/<int:pk>/` | CommentEditView | Edit comment |
| `/comment/delete/<int:pk>/` | CommentDeleteView | Delete comment |

### Search
| URL | View | Description |
|-----|------|-------------|
| `/search/` | SearchView | Search poems |
| `/search/load-more/` | SearchLoadMoreView | AJAX load more |

### About
| URL | View | Description |
|-----|------|-------------|
| `/about/` | AboutView | About page with stats |

---

## 🧪 Testing

Run the complete test suite:
```bash
python manage.py test
```

Run specific app tests:
```bash
python manage.py test accounts
python manage.py test poems
```

Test coverage includes:
- ✅ **Accounts:** Forms, Models, URLs, Views
- ✅ **Poems:** Forms, Models, URLs, Views
- ✅ **AJAX endpoints:** Load more, Like toggle
- ✅ **Permissions:** Login required, UserPassesTestMixin
- ✅ **Pagination:** 9 items per page

---

## 📈 Key Technical Decisions

### Why Django?
- **Rapid Development** - Built-in admin, ORM, and authentication
- **Security** - CSRF, XSS, SQL injection protection out of the box
- **Scalability** - Can handle growing content with proper indexing

### Why AJAX for Interactions?
- **Better UX** - No page reload for likes and comments
- **Performance** - Faster interactions
- **Modern Feel** - Smooth and responsive

### Why Auto-Publish?
- **Simplicity** - No need for moderation workflow
- **Immediate Feedback** - Users see their poems instantly
- **Community Building** - Encourages participation

### Why Infinite Scroll?
- **Better UX** - No pagination clicks
- **Mobile-Friendly** - Natural scrolling behavior
- **Engagement** - Keeps users browsing

### Why Bengali Interface?
- **Target Audience** - Bengali poetry lovers
- **Accessibility** - Lower barrier to entry
- **Cultural Connection** - Poetry is deeply cultural

### Why Custom Template Tags for Bengali Formatting?
- **Cultural Relevance** - Bengali users feel more at home
- **User Experience** - Numbers and dates in native script
- **Reusability** - Can be used across the entire application

### Why Management Commands?
- **Automation** - Easy setup for new installations
- **Consistency** - Predefined categories with proper structure
- **Documentation** - Clear list of available categories

### Why WhiteNoise for Static Files?
- **Simplicity** - No need for separate CDN or S3 bucket
- **Performance** - Compression and caching built-in
- **Cost** - No additional infrastructure costs

---

## 📧 Contact

- **Developer**: Soumyajit Guha
- **GitHub**: [guhasoumyajit67](https://github.com/guhasoumyajit67)
- **LinkedIn**: [guhasoumyajit67](https://linkedin.com/in/guhasoumyajit67)
- **Live Demo**: [https://lekhoni-by2b.onrender.com](https://lekhoni-by2b.onrender.com)

---

## 🙏 Acknowledgments

- Django community for the amazing framework
- All open-source libraries used in this project
- Bengali poetry lovers who inspired this platform

---

**Made with ❤️ for poetry lovers**