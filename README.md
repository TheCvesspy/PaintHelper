# MiniPaint Tracker

MiniPaint Tracker is a full-stack Python web application built with **Reflex** designed to help hobbyists manage their miniature painting projects, inventory, and guides.

## Features

### 🎨 Paint Inventory Management
- **Catalog System**: Manage a database of paints.
- **Inventory Tracking**: Keep track of owned paints (`owned_paints`) and custom mixtures (`custom_paints`).
- **Wishlist**: Maintain a shopping list of needed paints.

### 🖨️ Batch Printing Workflow
- **Project Organization**: Group print jobs into "Batches".
- **Job Tracking**: Manage individual print jobs and items within batches.
- **Status Updates**: Track the progress of your 3D printing tasks.

### 📚 Painting Guides
- **Step-by-Step Guides**: Create and follow custom painting guides.
- **Reference Images**: Integrate with Google Drive to store and view reference images.
- **Paint Mapping**: Link specific paints to guide steps.

### 🛠️ Admin & Dashboard
- **Dashboard**: Centralized hub for all activities.
- **User Management**: Authentication and registration system.
- **Admin Tools**: dedicated admin views for platform management.

## Tech Stack

- **Framework**: [Reflex](https://reflex.dev/) (Pure Python)
- **Database**: Supabase (PostgreSQL)
- **Storage**: Google Drive API
- **Deployment**: Google Cloud Run
