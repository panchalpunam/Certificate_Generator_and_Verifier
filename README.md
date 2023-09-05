
# Certificate Generator and Verifier

A web-based application for generating and verifying certificates easily.


## Table of Contents
- [About](#about)
- [Features](#features)
- [Demo](#demo)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Creating Certificates](#creating-certificates)
  - [Verifying Certificates](#verifying-certificates)



## About

The Certificate Generator and Verifier is a web application that allows users to create certificates by filling out a form and then verify those certificates using a unique code and a JWT token sent via email.

## Features

- Create certificates with custom information including name, course, date, signature, and subtitle.
- Generate PDF certificates from the provided data.
- Verify certificates using a unique code.
- Send verification links with JWT tokens via email.

## Demo

You can try the application live at [Demo Link](https://certificategeneartorandverifier.punampanchal.repl.co/).

## Getting Started

### Prerequisites

Before you begin, ensure you have the following:

- Python and pip installed.

## Install the required dependencies

To set up the required dependencies for this application, you can use the `requirements.txt` file provided in the project repository. Follow these steps:

1. Navigate to the project's root directory.

2. Run the following command to install the dependencies using `pip` (Python's package manager):

   ```bash
   pip install -r requirements.txt


### Installation

1. Clone this repository.

   ```sh
   git clone [https://github.com/your-username/certificate-generator.git](https://github.com/panchalpunam/Certificate_Generator_and_Verifier.git)



## Usage

  # Creating Certificates
      
  1. Visit the home page.

  2. Click on the "Create Certificate" button.

  3. Fill out the certificate details in the form, including name, course, date, signature, and subtitle.

  4. Click "Submit" to generate a PDF certificate.

  
  # Verifying Certificates

  1. Visit the home page.

  2. Click on the "Verify Certificate" button.

  3. Enter the certificate code.

  4. Click "Verify."

  5. An email will be sent to the recipient with a verification link containing a JWT token. The recipient can use this link to verify the certificate.
