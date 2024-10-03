
  
<h1 align="center"> Library Service Project </h1>  

 **Project Description**
 This project aims to modernize a local library's system for managing books, borrowings, users, and payments. Currently, the library's processes are outdated, relying on manual, paper-based tracking with no digital inventory system and only cash payments. The goal is to create a web-based system that simplifies administration, allows users to manage borrowings online, and supports digital payments via Stripe. 
 
 ## Features

### Functional Requirements:

1.  **Web-based system**
2.  **Book Management**:
    -   Add, update, and delete books.
    -   Manage book inventory.
3.  **Borrowing Management**:
    -   Borrow books, track borrowings, and return books.
4.  **User Management**:
    -   Register users and handle authentication.
5.  **Payment Handling**:
    -   Process payments through Stripe for borrowings and fines.
6.  **Notifications**:
    -   Send notifications via Telegram for new borrowings, overdue books, and successful payments.

### Non-functional Requirements:

-   Handle up to 5 concurrent users.
-   Support up to 1000 books and 50,000 borrowings per year.
-   Manage data efficiently (~30MB/year).

**JSON Web Tokens**: JSON Web Tokens are used to authenticate users.   
  
**Asynchronous Tasks with Celery and Flower**: The API includes a feature to schedule posts using Celery.

**Coverage tool**: use [Coverage.py](https://coverage.readthedocs.io/en/7.6.1/index.html). Coverage report: **93%**

## Security Checks 
This project includes automated security checks using two tools: **Bandit** and **Safety**. 
### Bandit 
- Bandit scans the codebase for potential security issues. 
- It generates an HTML report of the scan results. 
### Safety 
- Safety checks for known vulnerabilities in dependencies. 
- It requires an API key for its usage, which should be stored in an environment variable named `SAFETY_API_KEY`. 
- Similar to Bandit, it generates an HTML report of its findings. 
### Running Security Checks 
You can run the security checks by executing the following command: 
	```sh 
	python manage.py check
	```

### Notifications Service

Send notifications via Telegram for:

-   New borrowing creation
-   Borrowings overdue
-   Successful payments

## Installation  
  
1. **Clone the repository:**  
	 ```sh  
	  git clone https://github.com/AlexGrytsai/CityLibraryServiceAPI  
	 cd https://github.com/AlexGrytsai/CityLibraryServiceAPI  
	 ```
 2. **Environment Variables:**  
  Ensure you have a `.env` file in the root directory with the following variables:  
	 ```env
	 DJANGO_SECRET_KEY=DJANGO_SECRET_KEY  
	POSTGRES_PASSWORD=POSTGRES_PASSWORD  
	POSTGRES_USER=POSTGRES_PASSWORD  
	POSTGRES_DB=POSTGRES_PASSWORD  
	POSTGRES_HOST=db  
	POSTGRES_PORT=5432  
	PGDATA=/var/lib/postgresql/data  
	REDIS_HOST=redis
	CELERY_BROKER_URL=redis://redis:6379/0  
	CELERY_RESULT_BACKEND=redis://redis:6379/0  
	SAFETY_API_KEY=SAFETY_API_KEY  
	TELEGRAM_TOKEN=TELEGRAM_TOKEN  
	STAFFUSERS_CHAT_IDS=*******,*******,...  
	STRIPE_PUBLISHABLE_KEY=STRIPE_PUBLISHABLE_KEY  
	STRIPE_SECRET_KEY=STRIPE_SECRET_KEY
	 ```     
       
 3. **Build and start the application using Docker:**  
	 ```sh  
	  docker-compose up  
	 ```
 4. **Loading data into a database (examples):**  
  Open a new terminal and enter the command:  
	  ```sh
	  docker exec -it citylibraryserviceapi-app-1 /bin/sh
	  python manage.py loaddate example_data_for_db.json
	  ```

5. **Create a superuser:**  
	 ```sh  
	 python manage.py createsuperuser  
	 ```  
After created Super User, exit from container using the following command:  
	```sh 
	exit  
	```

 6. **Access the application:**  
  Open your web browser and navigate to [http://localhost:8000](http://localhost:8000) or [http://127.0.0.1:8000](http://127.0.0.1:8000).  
    You need to get access token for use app - [get token](http://127.0.0.1:8000/api/v1/token/).  
    For use an access token, you can use [ModHeader - Modify HTTP headers](https://chromewebstore.google.com/detail/modheader-modify-http-hea/idgpnmonknjnojddfkpgkljpfnnfcklj?pli=1) for Chrome. After installing it, you need added Authorization with "Bearer <your_access_token>".  
    Now, you can use all application's feathers.  
    Use Flower to monitor the status of scheduled tasks and other Celery workers - [http://localhost:5555](http://localhost:5555).  
      
7. **Access the application's documentation:**  
  You can familiarize yourself with all the documentation and methods of using the Airport API System by clicking on the link: [swagger](http://localhost:8000/api/v1/doc/swagger/).
