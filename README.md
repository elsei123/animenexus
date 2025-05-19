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

---

## Features

### Header
- The header highlights the **AnimeNexus** name, making the site immediately recognizable.
- Provides main navigation to sections such as *Home*, *About* and *Contact*.

<img width="1387" alt="header" src="https://github.com/user-attachments/assets/897b5888-2056-43db-9f91-85946ce7e564" />

### About Page
- Dedicated to explaining the site’s purpose and its context.

<img width="1054" alt="About Page" src="https://github.com/user-attachments/assets/7305fd57-703e-4d9d-bb8e-00cacbf48e12" />


### Contact Page
- Provides a simple form for users to send questions, suggestions, or feedback.

<img width="995" alt="Contact Page" src="https://github.com/user-attachments/assets/20ef7863-473f-49c7-80c8-394ba88698af" />


### Posts and Listings

- **Home Page**  
  - Lists featured posts or displays them in order by date/category.  
  - Shows the title, cover image, and a brief summary.

<img width="1435" alt="Home Page" src="https://github.com/user-attachments/assets/7136c238-3d3a-4390-a728-830dd544aea8" />


- **Post Detail Page**  
  - Displays the full post, including attached images and a comments section.
 
<img width="1126" alt="Post Detail Page" src="https://github.com/user-attachments/assets/703de32e-a710-47e2-83ea-e6b8aa22a823" />


- **Category Filter**  
  - Allows users to filter posts by specific topics (e.g., “Upcoming Releases,” “Best of the Year,” “Worse of All Time,” etc.).
 
    <img width="398" alt="Category Filter" src="https://github.com/user-attachments/assets/60608d2f-be62-4f0f-af90-feaae08f8489" />


### Comments
- A dedicated space for visitors to share opinions on the post’s topic.
- Can be moderated via the Django admin panel.

<img width="599" alt="comments section" src="https://github.com/user-attachments/assets/38ff412d-8fbf-4922-a46a-0104742b2079" />

---

## User Interaction Flow
1. **Visit Home**: Users see the most recent/featured posts.  
2. **Select a Post**: Click on a post to view full details.  
3. **Engage**: They can comment or navigate to other sections (About/Contact).  
4. **Return or Continue**: They may go back to Home, explore other categories.

---

## Features Left to Implement
- **Leaderboard/Ranking**: Display the most-read or most-commented posts to boost engagement.  
- **Timelined Updates**: Organize posts by anime seasons (Autumn, Winter, etc.).  
- **Multi-Language Support**: Make the platform available in additional languages (PT, JP, ES, FR).  
- **Additional Integrations**: Display event feeds, anime conventions, or streaming resources (Crunchyroll, Netflix).

---

## Testing

- **Browsers**: Tested on Chrome, Firefox, and Safari.  
- **Functionality**: Comments are saved correctly, links and categories work.  
- **Layout**: Verified on multiple screen sizes (smartphones, tablets, desktops).

 <img width="698" alt="testing" src="https://github.com/user-attachments/assets/50e4dc78-c1a3-43a4-988e-bfa8c5ce2fd8" />


---

## Validation

### HTML
- Validated via W3C Validator, with no markup errors.

### CSS
- Checked with the W3C Jigsaw Validator, with no markup errors.

### JavaScript
- Passed through JSHint.

### Python
- No erros were returned from PEP8

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

- **Image Bug**: In some posts, images do not appear correctly in the production environment, or are lost after server restarts. This is the only bug still unfixed.

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

## Credits

- **Knowledge Base**: Official Django documentation and the open-source community.  
- **Layout Inspiration**: User feedback and references from UI/UX for pop culture websites.  
- **Images and Assets**: Google images.
- **Cloudinary** for media hosting solutions.
- **Ebook**: Special thanks to the database structure ebook that served as a reference.  
- **Python Code**: Some logic snippets were inspired by Code Institute lessons ('I Think Therefore I Blog' and 'The Flask Framework'), adapted to this project.

