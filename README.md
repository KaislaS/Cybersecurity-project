# Cybersecurity-project

LINK: https://github.com/KaislaS/Cybersecurity-project/ 

To use the demo project, download the project files and run the following command: 

- Python manage.py runserver 

When the server is running, you can access the homepage by navigating to: http://127.0.0.1:8000/polls/ 

In the homepage you can answer multiple choice questions.  

If you want to access the admin interface or make changes to database, you can do that from http://127.0.0.1:8000/admin/ 

- Username: Admin 

- Password: SuperSecret123 

In the admin page you can add, edit and delete data, for example add new questions. You can also add or edit user accounts and permissions. 

There are 5 cybersecurity flaws in the code, and I have implemented these flaws from the OWASP Top Ten list of 2017. In addition, I have included a CSRF vulnerability, which is not in this list. To use this demo project, you need to have Django and Python 3 installed. 

 

## Flaw 1: Cross-Site Scripting (XSS) 

### Flaw:  

https://github.com/KaislaS/Cybersecurity-project/blob/main/polls/templates/polls/detail.html#L14 

https://github.com/KaislaS/Cybersecurity-project/blob/main/polls/views.py#L71 

https://github.com/KaislaS/Cybersecurity-project/blob/main/polls/models.py#L10 

 

### Fix:  

https://github.com/KaislaS/Cybersecurity-project/blob/main/polls/templates/polls/detail.html#L12 

https://github.com/KaislaS/Cybersecurity-project/blob/main/polls/views.py#L74 

https://github.com/KaislaS/Cybersecurity-project/blob/main/polls/models.py#L9 

 

XSS is a type of security vulnerability where an attacker can inject malicious scripts, for example JavaScript or HTML code into web pages and these scripts are often executed in the browser of anyone viewing the page. That allows attackers to data theft, and they can for example steal session cookies. Phishing is also possible, where attacker redirects users to fake pages to steal credentials. XSS vulnerability allows attackers to modify how the site looks or behaves. XSS attacks can occur when user input is not properly sanitized or escaped [1]. 

In this project, user input was displayed with the “| safe” filter, which allows scripts to be executed in the user’s browser. 

In the fix, the “| safe” filter was removed to ensure that the question text is properly escaped, and it will be displayed as a plain text instead of being interpreted as HTML or JavaScript. 

 

 

## Flaw 2: Sensitive Data Exposure 

 

### Flaw: 

https://github.com/KaislaS/Cybersecurity-project/blob/main/polls/views.py#L78 

https://github.com/KaislaS/Cybersecurity-project/blob/main/mysite/settings.py#L26 

 

 

### Fix: 

https://github.com/KaislaS/Cybersecurity-project/blob/main/polls/views.py#L85 

https://github.com/KaislaS/Cybersecurity-project/blob/main/mysite/settings.py#L29 

 

 

Sensitive Data Exposure occurs when an application inadvertently exposes sensitive information, such as passwords, credit card numbers, or secret keys, to unauthorized users. This can happen through various means, including improper error messages, logging, or hardcoding sensitive data in the source code [2]. 

 

In this project, the sensitive data exposure flaw was demonstrated by directly exposing the Django secret key in an HTTP response when you navigate to /polls/sensitive_data/. Hardcoding such sensitive information can expose it to attackers, especially if the code is pushed to a public repository (such as Git). If an attacker gains access to this key, they can impersonate users, perform session hijacking, or even forge secure data. 

 

To fix this I avoided exposing the sensitive information in the response and used environment variables to securely manage sensitive data. I created a .env file to store the secret key and used the python-dotenv package to load the environment variables ins settings.py. I also modified the view to avoid exposing the secret key. Now sensitive information is securely managed and not exposed to unauthorized users. 

 

 

 

 

## Flaw 3: Security Misconfiguration  

 

### Flaw: 

https://github.com/KaislaS/Cybersecurity-project/blob/main/mysite/settings.py#L33 

 

### Fix: 

https://github.com/KaislaS/Cybersecurity-project/blob/main/mysite/settings.py#L37 

 

 

Security Misconfiguration occurs when a system is not securely configured, making it vulnerable to attacks. This includes issues like overly permissive settings, default credentials, unnecessary services, or incorrect file permissions. It often results from leaving security settings at their defaults or improperly configuring them during development or deployment [3]. 

In my project, I leave debug mode or verbose error messages enabled in production, and it exposes detailed error messages (such as stack traces, URL patterns, and environment details) in production and can leak sensitive information like project structure, database paths, or installed apps, which can aid attackers in compromising the system. Fix in my project is that I disable debug mode in production environments. 

 

## Flaw 4: Cross-Site Request Forgery (CSRF) 

### Flaw: 

https://github.com/KaislaS/Cybersecurity-project/blob/main/polls/views.py#L43 

https://github.com/KaislaS/Cybersecurity-project/blob/main/polls/views.py#L90 

https://github.com/KaislaS/Cybersecurity-project/blob/main/polls/templates/polls/malicious.html 

https://github.com/KaislaS/Cybersecurity-project/blob/main/polls/templates/polls/index.html#L18 

https://github.com/KaislaS/Cybersecurity-project/blob/main/polls/templates/polls/detail.html#L10 

 

### Fix: 

https://github.com/KaislaS/Cybersecurity-project/blob/main/polls/views.py#L42 

https://github.com/KaislaS/Cybersecurity-project/blob/main/polls/templates/polls/detail.html#L9 

 

CSRF (Cross-Site Request Forgery) is an attack where a malicious user tricks an authenticated user into performing unintended actions on a website. This occurs when a user is tricked into making a request that they did not intend to, using their authenticated session [4]. 

In my project, the {% csrf_token %} tag is missing, and this can result in unauthorized actions, such as making transactions, without the user’s consent. In this case, user answers question without their consent.  On the homepage, there is a button that entices users to click in hopes of a reward. When clicked, the user is redirected to a malicious HTML page and is made to answer a question without consent. To fix the problem every state-changing request (POST, PUT, DELETE) must include a valid CSRF token, which can be validated by the server to confirm the legitimacy of the request. 

 

## Flaw 5: Broken Authentication  

### Flaw: https://github.com/KaislaS/Cybersecurity-project/blob/main/polls/views.py#L63 

### Fix: https://github.com/KaislaS/Cybersecurity-project/blob/main/polls/views.py#L66 

Broken authentication happens when an application incorrectly handles user authentication or session management, allowing attackers to bypass authentication or impersonate users. Attackers need access to a few accounts, or just one admin account, to compromise the system, potentially enabling fraud, identity theft, or exposure of sensitive information [5]. 

Broken Authentication flaw in my project is that an attacker can vote multiple times (as a user) or impersonate another user without any form of authentication or session management. To fix this, I have to authenticate users and restrict voting to one vote per user. 

 

### References: 

[1]: https://owasp.org/www-project-top-ten/2017/A7_2017-Cross-Site_Scripting_(XSS) 

[2]: https://owasp.org/www-project-top-ten/2017/A3_2017-Sensitive_Data_Exposure 

[3]: https://owasp.org/www-project-top-ten/2017/A6_2017-Security_Misconfiguration 

[4]: https://owasp.org/www-community/attacks/csrf  

[5]: https://owasp.org/www-project-top-ten/2017/A2_2017-Broken_Authentication 
