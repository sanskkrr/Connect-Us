Connect-Us — Social Media & Real-Time Chat App

A full-stack social media application with real-time messaging built using Django and modern web technologies.



🌐 Live Demo

👉 [Add your deployed link here]

💻 GitHub Repository

👉 https://github.com/your-username/your-repo



📌 Features
	•	🔐 User Authentication (Login, Register, Password Reset)
	•	👥 Follow / Unfollow Users
	•	💬 Real-time One-to-One Chat (WebSockets)
	•	💾 Persistent Message Storage (PostgreSQL)
	•	🖼️ Image Upload (Cloudinary)
	•	📱 Responsive UI (Tailwind CSS)
	•	📨 Messages Section with User List



🛠️ Tech Stack

Backend:
	•	Django
	•	Django Channels (WebSockets)

Database:
	•	PostgreSQL

Frontend:
	•	HTML, CSS, Tailwind CSS

Media Storage:
	•	Cloudinary

Deployment:
	•	Render



⚙️ Installation (Local Setup)

git clone https://github.com/your-username/your-repo.git
cd your-repo

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt



🔑 Environment Variables

Create a .env file in root:

SECRET_KEY=your_django_secret
DATABASE_URL=your_postgres_url
CLOUD_NAME=your_cloudinary_name
API_KEY=your_cloudinary_api_key
API_SECRET=your_cloudinary_api_secret



🧪 Run Locally

python manage.py migrate
python manage.py runserver

For WebSockets:

daphne projectFolder.asgi:application



🚀 Deployment
	•	Hosted on Render
	•	PostgreSQL database
	•	Cloudinary for media storage
	•	WhiteNoise for static files



📚 What I Learned
	•	Real-time systems using WebSockets
	•	Django backend architecture
	•	Authentication & user relationships
	•	PostgreSQL database handling
	•	Debugging full-stack issues



📈 Future Improvements
	•	Unread message system
	•	Online/offline status
	•	Typing indicator
	•	Message pagination
