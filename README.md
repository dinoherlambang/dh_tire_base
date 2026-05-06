# Centralized Tire Base Management (`dh_tire_base`)

## Overview
`dh_tire_base` is the foundational module for the Dino Hub Tire Management ecosystem. It centralizes master data and core tracking logic that is shared across multiple dependent modules, including the Tire Management System (TMS), Retread Production, and Field Reports. 

By unifying the tire specifications and tracking flags within the core `stock.production.lot` model, this module ensures consistency, prevents data duplication, and loosely couples downstream applications.

## Key Features

### 1. Centralized Tire Master Data
Provides standalone models for standardized tire nomenclature:
- **Tire Brand** (`dh.tire.brand`): Manages tire manufacturers (e.g., Michelin, Bridgestone).
- **Tire Size** (`dh.tire.size`): Standardizes tire dimensions (e.g., 1000R20, 11R22.5).
- **Tire Pattern** (`dh.tire.pattern`): Tracks tread patterns, linked directly to their respective Brands.

### 2. Enhanced Serial Number Tracking (`stock.production.lot`)
This module extends the standard Odoo lot/serial number system to support tire-specific life cycles:
- **Classification (`is_tire`)**: A computed flag that determines whether a serial number represents a tire. When checked, it exposes tire-specific fields on the Lot view.
- **Physical Specifications**: Links the lot directly to the `tire_brand_id`, `tire_size_id`, and `tire_pattern_id` master data.
- **Universal Metrics**: 
  - `retread_count`: Tracks how many times a tire casing has been retreaded.
- **Global Lifecycle Status (`tire_status`)**: Tracks the high-level location and state of the tire across all departments:
  - `new`: New Tire
  - `mounted`: Mounted on Vehicle
  - `unmounted`: Unmounted / In Warehouse
  - `retread`: In Retreading
  - `scrapped`: Scrapped

## Technical Details

### Dependencies
- `stock`: Relies heavily on the `stock.production.lot` model to act as the single source of truth for individual tires.

### Downstream Modules
The following modules depend on `dh_tire_base` or use its data structure:
- `dh_tms` (Tire Management System)
- `dh_tire_retread_production` (Tire Retreading & Work Orders)
- `dh_field_report` (Field Damage & Inspection Reports)

### Development Notes
- **Computed Fields & Readonly Behavior**: The `is_tire` field is automatically calculated based on the product category (looking for the words 'tire' or 'ban'). However, it has been deliberately configured with an `inverse` method and `readonly="0"` in the view. This allows users to manually check or uncheck the flag if the automatic categorization fails.
- **Data Migration Hook**: Contains a `post_init_hook` (`_migrate_existing_tire_data`) in `migrations/migrate_data.py` designed to sweep existing tire data from legacy modules and safely populate the new centralized schema during installation.

## Installation
Simply install the module from the Odoo Apps menu. Ensure that any legacy module references to old text-based fields (e.g., `tire_brand`, `casing_size`) have been migrated or mapped correctly before installing dependent apps.
