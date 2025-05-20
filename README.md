# AnimeNexus

**AnimeNexus** is an interactive web application focused on creating, reading, and discussing anime, manga, and the broader Japanese pop culture universe. It provides a platform where users can explore posts, comment, and engage with different anime-related content in an intuitive, responsive way.

The application is built using **Django (Python)**, **HTML**, **CSS**, and **JavaScript**, ensuring a fast and user-friendly experience. The main mission of **AnimeNexus** is to offer a welcoming environment where anime fans can **share ideas**, **discover new titles**, and **further immerse themselves** in the otaku community.

---

## Key Features

### Interactivity and Engagement
- Users can read posts about anime and manga.
- Comments are supported, allowing discussions and opinion exchanges.
- A category system is integrated to filter posts by specific topics.

### Post Management
- **CRUD** (Create, Read, Update, Delete) functionality for posts, with the ability to include cover images for each anime.
- Immediate feedback in the Django admin panel for managing posts and comments.

### Responsive and Accessible
- A layout adaptable to any screen size: desktops, tablets, and smartphones.
- Intuitive navigation, ensuring ease of use for different age groups and skill levels.


## Core Technologies

### Django (Python)
- Provides the entire backend structure and database integration.
- Robust route, model, and **Admin Panel** management.

### HTML
- Structures and semantically marks up pages, enhancing accessibility and SEO.

### CSS
- Styles the application, ensuring a visually pleasing experience and cohesive identity.
- Implements responsive design for various screen resolutions.

### JavaScript
- Manages dynamic interactions.

### Cloudinary 
- For media storage

### Gunicorn & Whitenoise
- For production static serving

---

## Features

### Header
- The header highlights the **AnimeNexus** name, making the site immediately recognizable.
- Provides main navigation to sections such as *Home*, *Categories*, *About*, *Contact* and *Login*.

<img width="1006" alt="Header" src="https://github.com/user-attachments/assets/58a6ca7c-66e1-486c-9348-d8247edb9ba8" />


### About Page
- Dedicated to explaining the site’s purpose and its context.

<img width="874" alt="About" src="https://github.com/user-attachments/assets/9cf6f0fb-2a9b-46e8-a13c-5919a45cfeff" />


### Contact Page
- Provides a simple form for users to send questions, suggestions, or feedback.

<img width="508" alt="contact" src="https://github.com/user-attachments/assets/4066199f-7c5b-4e3a-be9b-21be95f0cb2d" />


### Posts and Listings

- **Home Page**  
  - Lists featured posts or displays them in order by date/category.  
  - Shows the title, cover image, and a brief summary.

      <img width="844" alt="Home page" src="https://github.com/user-attachments/assets/9cfa29d5-53f3-485e-8980-332113667306" />


- **Post Detail Page**  
  - Displays the full post, including attached images and a comments section.
 
      <img width="556" alt="Post Detail Page" src="https://github.com/user-attachments/assets/6fb73e9f-93cf-422e-8d03-2bc63ef05c92" />



- **Category Filter**  
  - Allows users to filter posts by specific topics (e.g., “Upcoming Releases,” “Best of the Year,” “Worse of All Time,” etc.).
 
    <img width="340" alt="Category Filter" src="https://github.com/user-attachments/assets/6ef7c0c8-8104-4103-b456-01d737892c96" />



### Comments
- A dedicated space for visitors to share opinions on the post’s topic, firt they need to login.
- Can be moderated via the Django admin panel.

<img width="261" alt="comments section" src="https://github.com/user-attachments/assets/e7ade89f-3fdf-449a-a13f-7aa1de200192" />

<img width="359" alt="comments section after login" src="https://github.com/user-attachments/assets/2808fc79-b61e-4f7d-a45d-b59f25a1a19a" />

---

## User Interaction Flow
1. **Visit Home**: Users see the most recent/featured posts.  
2. **Select a Post**: Click on a post to view full details.  
3. **Engage**: They can comment or navigate to other sections (About/Contact).  
4. **Return or Continue**: They may go back to Home, explore other categories.

---

## Agile Workflow & UX Design

- See [Agile Documentation](https://github.com/elsei123/animenexus/blob/main/docs/ux1/Agile_Workflow_%26_UX_Design_Documentation.md) for:

- Epics, User Stories & Tasks

- Board Mapping (Backlog, To Do, In Progress, Done)

- Information Hierarchy, Wireframes & Mockups, and Design Rationale

---

## Testing

- **Browsers**: Tested on Chrome, Firefox, and Safari.  
- **Functionality**: Comments are saved correctly, links and categories work.  
- **Layout**: Verified on multiple screen sizes (smartphones, tablets, desktops).

<img width="735" alt="Lighthouse Testing" src="https://github.com/user-attachments/assets/27dd730e-f00d-413b-9d18-daff2dd8fd9d" />

### Python Tests

#### Key Test Scenarios Covered:

- **Post CRUD & Permissions**: Verified create, edit, delete flows with @login_required and ownership checks.

- **Comment Management**: Tested comment submission requiring login, edit and delete with correct context and view fixes.

- **Signup Flow**: Confirmed user and profile creation, auto-login, and welcome message via SignUpForm tests.

- **Contact Form**: Mocked send_email_via_emailjs for success and failure paths, ensuring appropriate feedback messages.

- **Profile View**: Handled both own and other user profiles, auto-creating missing Profile instances.

#### Common Issues & Fixes:

- Missing context in edit_comment view: tests failed with NoReverseMatch until the comment object was passed into the template context.

- Incorrect signature in profile view: NameError: username fixed by adding username=None parameter and unifying both definitions.

- Assertion adjustments: replaced assertQuerysetEqual with assertEqual(list(...), []) for comments list.

- Message punctuation: updated tests to expect periods instead of exclamation marks for success messages ('Post created successfully.', 'Post deleted successfully.').




---

## Validation

### HTML
- Validated via W3C Validator, with no markup errors.

### CSS
- Checked with the W3C Jigsaw Validator, with no markup errors.

### JavaScript
- Linted and unit-tested with Jest & Testing Library.

### Python
- No erros were returned from PEP8 (flake8)

---

## Bug Fixes

1. **Ephemeral File System on Heroku**  
   - **Context**: Storing images locally in Heroku caused them to disappear after dynos were restarted.  
   - **Solution**: Integrated a cloud-based storage (Cloudinary) and updated settings for persistent image handling.

2. **`collectstatic` Deploy Error**  
   - **Context**: The `collectstatic` command failed during deployment due to improper `STATIC_ROOT` configuration.  
   - **Solution**: Specified `STATIC_ROOT` in `settings.py` and verified all static file paths. This ensured that static assets (CSS, JS, etc.) were compiled and served correctly in the Heroku environment.

3. **Templates Not Found**  
   - **Context**: Custom `templates/` folder wasn't recognized by Django, resulting in “TemplateDoesNotExist” errors.  
   - **Solution**: Adjusted the `TEMPLATES` setting in `settings.py` to correctly point to the `templates/` directory and verified each app’s template structure.

4. **Broken Routes in `urls.py`**  
   - **Context**: Certain endpoints conflicted or appeared in the wrong order, causing 404 errors.  
   - **Solution**: Reorganized the URL patterns, placing more specific routes before generic ones and ensuring the correct views were assigned.

5. **Image Upload and Cloudinary Mapping**  
   - **Context**: Moving from local media storage to Cloudinary led to outdated references (e.g., `/media/...`) in the database, plus some images exceeded the Cloudinary size limit.  
   - **Solution**: Cleaned up older records to point to the new Cloudinary URLs and enforced file-size checks prior to upload, preventing silent failures.


---

## Unfixed Bugs

- No known bugs remain at this time.

---

## Deployment

**AnimeNexus** is currently live on Heroku:  
- [AnimeNexus on Heroku](https://animenexus-cfbf85db2b0e.herokuapp.com/)

### Deployment Steps Heroku
1. Heroku: Log into the Heroku dashboard.  
2. New App: Click New → Create new app.
3. Settings > Config Vars: Add all required environment variables
4. Connect the GitHub repository to Heroku via the Deploy tab.  
5. Use automatic deployment from GitHub to push changes.  
6. The app becomes accessible at the generated link, ready for use.

---

## Features Left to Implement
- **Leaderboard/Ranking**: Display the most-read or most-commented posts to boost engagement.  
- **Timelined Updates**: Organize posts by anime seasons (Autumn, Winter, etc.).  
- **Multi-Language Support**: Make the platform available in additional languages (PT, JP, ES, FR).  
- **Additional Integrations**: Display event feeds, anime conventions, or streaming resources (Crunchyroll, Netflix).

---

## Credits

- **Knowledge Base**: Official Django documentation and the open-source community.  
- **Layout Inspiration**: User feedback and references from UI/UX for pop culture websites.  
- **Images and Assets**: Google images.
- **Cloudinary** for media hosting solutions.
- **Ebook**: Special thanks to the database structure ebook that served as a reference.  
- **Python Code**: Some logic snippets were inspired by Code Institute lessons ('I Think Therefore I Blog' and 'The Flask Framework'), adapted to this project.

