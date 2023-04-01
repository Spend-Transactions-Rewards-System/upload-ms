<a name="readme-top"></a>


<!-- PROJECT LOGO -->
<br />
<div align="center">
<h3 align="center">ITSA G1 T3 Project B AY2022/23 Semester 2</h3>

  <p align="center">
    Upload Microservice
    <br />
    <a href="https://itsa-t3-upload-ms.stoplight.io/docs/upload-ms/branches/main/9ae56e8b59f9f-upload-ms"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://www.itsag1t3.com">View Demo</a>
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Microservice
Reward programs are becoming a popular marketing tool for banks and credit card issuers to attract and retain customers. Our application provides customers with an efficient and user-friendly platform for managing their rewards. A large number of spend transactions can be processed daily in real-time and the application is able to accept these transactions via a file upload or API request to the tenant. Campaign management is available for tenants, where they can run customisable campaigns for specific card programs that encourage user spending, while at the same time reward customers. From a customer perspective, this enhances the perceived value of these card programs offered by the tenant, helping our affiliated banks to preserve brand loyalty and expand their market share.

The upload microservice aims to provide functionalities to handle large file validation and file uploads to the cloud for other services to retrieve it for further processing.


### Built With

* [![Flask][Flask.com]][Flask-url]
* [![AWS S3][AWS.com]][AWS-url]



<!-- GETTING STARTED -->
## Getting Started
### Prerequisites
1. Create a table in Dynamodb
2. Create 2 AWS S3 buckets, one to store spend files and one to store user files.
3. For each S3 bucket, create 3 folders named "raw", "processed" and "error".
3. Retrieve _**Access Key ID**_ and _**Secret Access Key**_ from your IAM user


### Installation (Linux)
1. Clone the repo
   ```sh
   git clone https://github.com/cs301-itsa/project-2022-23t2-g1-t3-be-upload-ms.git
   ```
2. Change directory into the repo
    ```sh
    cd project-2022-23t2-g1-t3-be-upload-ms
    ```
3. Create virtual environment and install project dependencies
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
4. Create an environment file and add your environment variables
   ```sh
   nano ./src/view/.env
   ```
   Replace variables in curly braces with your own credentials
   ```txt
   ACCESS_KEY_ID={AWS Access Key ID}
   SECRET_ACCESS_KEY={AWS Secret Access Key}
   REGION={AWS Region}
   DYNAMODB_TABLE_NAME={AWS Dynamodb Table Name}
   USER_S3_BUCKET_NAME={AWS User S3 bucket name}
   SPEND_S3_BUCKET_NAME={AWS Spend S3 bucket name}
   ```
5. Run the microservice
   ```sh
   python wsgi.py
   ```
<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

### Team Members
* Sean Tan
* Joshua Zhang
* Tan Gi Han
* Stanford
* Hafil
* Dino
* Gan Shao Hong

### Project Advisor/Mentor
* [Professor Ouh Eng Lieh](https://www.linkedin.com/in/eng-lieh-ouh/?originalSubdomain=sg)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

[AWS-url]: https://aws.amazon.com/s3/
[AWS.com]: https://img.shields.io/badge/Amazon_AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/en/2.2.x/
[Flask.com]: https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white