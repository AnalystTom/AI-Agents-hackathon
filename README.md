# Product Recommendation using AI Agents


**Introduction**
The AI-Powered Product Recommender System is an innovative application that leverages advanced AI models to provide personalized product recommendations based on natural language user input. By integrating OpenAI's GPT models with a robust backend and interactive frontend, the system offers users an intuitive and engaging shopping experience.

**Features**
Natural Language Understanding: Users can input queries in natural language, and the system accurately interprets their intent.
Personalized Recommendations: Generates tailored product suggestions based on user preferences, history, and feedback.
User Interaction History: Tracks user interactions to enhance recommendation accuracy over time.
Real-Time Feedback Integration: Allows users to like or dislike products, refining future recommendations.
Scalable Architecture: Built with scalability in mind, suitable for deployment on cloud platforms.
Architecture

<img width="512" alt="image" src="https://github.com/user-attachments/assets/c27553dd-e6d0-4fb6-b0a6-59a1a0000144">


The system comprises the following components:

**Frontend**: A React.js application that provides an interactive user interface.
**Backend**: A FastAPI server that handles API requests and orchestrates interactions between components.
**AI Agents:**
**NLP Agent**: Processes user input using OpenAI's GPT models to extract intent and preferences.
**Recommendation Agent:** Generates personalized product recommendations.
**Database:** Google Cloud SQL (MySQL) database storing product data, user interactions, and feedback.
**OpenAI API:** Utilized by AI agents for advanced language processing capabilities.


**Demo**
Include screenshots or GIFs of your application in action.

**Technology Stack**
Frontend:
React.js
JavaScript (ES6+)
CSS (or CSS-in-JS libraries)
Backend:
FastAPI
Python 3.9+
MySQL Connector for Python
AI Integration:
OpenAI GPT-3.5 via OpenAI API
Database:
Google Cloud SQL (MySQL)
Hosting and Deployment:
Backend: Google Cloud Run
Frontend: Firebase Hosting
Tools and Services:
Docker
Git and GitHub
Visual Studio Code
Installation
Prerequisites
Node.js (v14 or later)
Python (3.9 or later)
npm (comes with Node.js)
Google Cloud Account with billing enabled
OpenAI API Key
Backend Setup
Clone the Repository

**How to run the code**

git clone https://github.com/yourusername/product-recommender-system.git
cd product-recommender-system/backend
Create a Virtual Environment

2.
python3 -m venv venv
source venv/bin/activate
Install Dependencies

3.
pip install -r requirements.txt
Set Environment Variables

Create a .env file in the backend directory:

4.
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name
CLOUD_SQL_CONNECTION_NAME=your_cloud_sql_connection_name
OPENAI_API_KEY=your_openai_api_key
Run the Backend Server

5.
uvicorn app.main:app --reload --port 8000
Frontend Setup
Navigate to the Frontend Directory

6.
cd ../frontend
Install Dependencies

7.
npm install
Set Environment Variables

Create a .env file in the frontend directory:

8.
REACT_APP_API_URL=http://localhost:8000
Run the Frontend Application

9.
npm start
AI Agents Setup
Navigate to the AI Agents Directory

10.
cd ../ai_agents
Create a Virtual Environment

11.
python3 -m venv venv
source venv/bin/activate
Install Dependencies

12.
pip install -r requirements.txt
Set Environment Variables

13.
OPENAI_API_KEY=your_openai_api_key
Database Setup
Set Up Google Cloud SQL

14.
Create a MySQL instance on Google Cloud SQL.
Configure network and authentication.
Initialize the Database



15.
cd ../scripts/database_setup
python create_tables.py
python seed_data.py
Usage
Access the Application

16.
Open your browser and navigate to http://localhost:3000.
Enter a Product Query

**App Flow:**
Use natural language to describe what you're looking for.
Example: "I'm searching for a waterproof smartwatch under $200 for swimming."
View Recommendations

The system will display personalized product recommendations based on your input.
Provide Feedback

Like or dislike products to help the system refine future recommendations.
Explore Products


We welcome contributions to enhance the functionality and features of this project. To contribute:

Fork the Repository

Click on the "Fork" button at the top right of the repository page.

Clone Your Fork

bash
Copy code
git clone https://github.com/yourusername/product-recommender-system.git
Create a Branch

bash
Copy code
git checkout -b feature/your-feature-name
Make Your Changes

Follow the existing code style and conventions.
Write clear and concise commit messages.
Push to Your Fork

bash
Copy code
git add .
git commit -m "Add your commit message here"
git push origin feature/your-feature-name
Create a Pull Request

Go to the original repository and click on "Pull Requests."
Submit your pull request for review.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
OpenAI for providing the GPT models and API access.
Google Cloud Platform for hosting and database services.
Contributors who have helped in developing and improving this project.
Community for support and inspiration.
Feel free to reach out if you have any questions or need assistance with the setup.


Discord: russki_boi_vlad
