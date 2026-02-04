# Test Plan - MiniPaint Tracker

## Credentials
**User**: `cvesspy@gmail.com`
**Pass**: `gyn9zjf-jqn4ZHA6kmh`

## 1. Regression Testing
Scenarios to verify core application stability.

### 1.1 Authentication
- [ ] Login with valid credentials (`cvesspy@gmail.com`).
- [ ] Verify redirection to Dashboard.
- [ ] Verify session persistence on refresh.

### 1.2 Dashboard Navigation
- [ ] Verify "Print Jobs" tab loads.
- [ ] Verify "Paints Library" tab loads.
- [ ] Verify "Owned Paints" tab loads.
- [ ] Verify "Painting Guides" tab loads.

## 2. New Feature: Painting Guides
Verification of the enhanced Painting Guide creation flow (`Layering` and `Contrast` modes).

### 2.1 Guide Creation (Happy Path)
- [x] **Create Layering Guide**:
    - Click "New Guide".
    - Select Mode: "Layering".
    - Enter Name (e.g., "Space Marine Armor").
    - Select Primer from Owned Paints.
    - Add Step "Basecoat" -> Select Paint.
    - Save.
    - **Expected**: Guide appears in list. Modal closes.

- [x] **Create Contrast Guide**:
    - Click "New Guide".
    - Select Mode: "Contrast".
    - Enable "Slapchop".
    - Add Step "Skin" -> Select Paint (Role: Contrast).
    - Save.
    - **Expected**: Guide appears with "Contrast" badge.

### 2.2 Paint Selection & Modal Interaction
- [x] **Open Paint Selector**:
    - In "New Guide" modal, click "Add" on a paint slot.
    - **Expected**: Paint Selection overlay appears.
- [x] **Select Paint**:
    - Search for an owned paint.
    - Click "Select".
    - **Expected**: Overlay closes, paint is added to the slot with correct role.
- [x] **Cancel Selection**:
    - Open Selector -> Click "Cancel".
    - **Expected**: Overlay closes, no paint added.

### 2.3 Error Handling & State (Bug Fixes)
- [x] **Unsaved Changes Protection**:
    - Open New Guide -> Enter Name.
    - Click "Cancel" or "X".
    - **Expected**: "Discard Changes?" Confirmation Dialog appears.
    - Click "Continue Editing" -> Modal stays open.
    - Click "Discard" -> Modal closes.
- [x] **Save Logic**:
    - Attempt to save without Name.
    - **Expected**: Error Toast "Guide Name is required".
    - Attempt to save with network error/RLS issue.
    - **Expected**: Error Toast (and debug log output).

## 3. Database & RLS
- [x] Verify `painting_guides` insertion behaves correctly for ownership (`user_id`).
- [x] Verify Cascade Delete: Deleting a guide removes its details and paints.
