# briefings_management

A Briefing is the document that describes a project to be
developed by a Supplier, based on the survey carried out with the Customer,
where it describes the contractual premises and attributes of each of the products to be
be produced.

## Getting Started

### Prerequisites

Before starting, make sure you have installed:
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/install/)

Check that they are installed correctly using the following commands:

```bash
docker --version
docker-compose --version
```

### Clone the repository
Follow these steps to set up your development environment:

1. Clone the repository:
    ```bash
    git clone [git@github.com:jarrthur/briefings_management.git](https://github.com/jarrthur/briefings_management.git)
    ```
2. Navigate to the project directory:
   ```cmd
   cd briefings_management
   ```

### Build and run with Docker
```bash
docker-compose up --build
```
In this operation, the following commands are automatically executed:

1. Apply migrations
2. Run the Django command that creates the initial categories
3. Check if Superuser already exists in the application, otherwise, create it with the following fields:
```
Username: admin
Password: admin
```
4. Start the application
5. **Optional**: You can add items via the `/admin/` url with the credentials already created


## API Endpoints

This project includes the following API endpoints for managing Briefings, Retailers, Vendors, and Categories.

### Briefing Endpoints

- **List Briefings**
  - **URL**: `/api/briefings/`
  - **Method**: `GET`
  - **Description**: Returns a list of all briefings.

- **Create Briefing**
  - **URL**: `/api/briefing/`
  - **Method**: `POST`
  - **Description**: Creates a new briefing.

- **Detail/Update Briefing**
  - **URL**: `/api/briefing/<int:id>/`
  - **Method**: `GET`, `PUT`
  - **Description**: Returns details of a specific briefing or updates an existing briefing.

### Retailer Endpoints

- **List Retailers**
  - **URL**: `/api/retailers/`
  - **Method**: `GET`
  - **Description**: Returns a list of all retailers.

- **Create Retailer**
  - **URL**: `/api/retailer/`
  - **Method**: `POST`
  - **Description**: Creates a new retailer.

- **Detail/Update Retailer**
  - **URL**: `/api/retailer/<int:id>/`
  - **Method**: `GET`, `PUT`
  - **Description**: Returns details of a specific retailer or updates an existing retailer.

### Vendor Endpoints

- **List Vendors**
  - **URL**: `/api/vendors/`
  - **Method**: `GET`
  - **Description**: Returns a list of all vendors.

- **Create Vendor**
  - **URL**: `/api/vendor/`
  - **Method**: `POST`
  - **Description**: Creates a new vendor.

- **Detail/Update Vendor**
  - **URL**: `/api/vendor/<int:id>/`
  - **Method**: `GET`, `PUT`
  - **Description**: Returns details of a specific vendor or updates an existing vendor.

### Category Endpoints

- **List Categories**
  - **URL**: `/api/categories/`
  - **Method**: `GET`
  - **Description**: Returns a list of all categories.

- **Create Category**
  - **URL**: `/api/category/`
  - **Method**: `POST`
  - **Description**: Creates a new category.

- **Detail/Update Category**
  - **URL**: `/api/category/<int:id>/`
  - **Method**: `GET`, `PUT`
  - **Description**: Returns details of a specific category or updates an existing category.

## Tests
You can execute all tests in the project with the followings commands:
 
- Navigate to the directory containing the Django manage.py file
```cmd
 cd briefing_management
```

- Run the command to run the tests
```bash
python manage.py test
```

## Main feature
Customization of the original AutoSchema to adapt the requirements of the api description in file [desc_api.yaml](desc_api.yaml) , using [drf-specatular](https://drf-spectacular.readthedocs.io/en/latest/), overwriting the api descriptions according to their respective models.

Customization can be found at: [schemas.py](./briefing_management/base/schemas.py)
