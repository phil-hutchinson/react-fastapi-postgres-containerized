# Multi-Tenant Implementation Game Plan

## Overview
Implement multi-tenancy with tenant_id + path-based routing (`/tenant1/api/notes`) in incremental steps. Each step leaves the system fully functional with all tests passing.

## Strategy
- Path-based tenant routing: `/tenant1`, `/tenant2`, etc.
- Shared database schema with `tenant_id` column
- Default tenant for backward compatibility during migration
- No authentication/authorization initially (just path-based access)

---

## Phase 1: Database Foundation (Invisible to Users)

### Step 1: Add Tenants Table & Default Tenant ✅ COMPLETE
**Goal**: Create tenant infrastructure without breaking existing functionality

**Changes**:
- [x] Create `tenants` table with columns:
  - `id` (UUID, primary key)
  - `slug` (string, unique) - URL-friendly identifier (e.g., "acme", "demo")
  - `name` (string) - Display name
  - `created_at` (timestamp)
  - `is_active` (boolean, default true)
- [x] Create Alembic migration
- [x] Seed with default tenant: `slug="default"`, `id="00000000-0000-0000-0000-000000000000"`
- [x] Create `Tenant` SQLAlchemy model in `backend/models/tenant.py`

**Testing**:
- [x] All existing tests pass (no changes to app behavior yet)
- [x] Verify tenant table created and seeded

**User Impact**: None - system works exactly as before

---

### Step 2: Add tenant_id to Notes Table ✅ COMPLETE
**Goal**: Add tenant_id column, maintain existing functionality with app-level defaults

**Changes**:
- [x] Create Alembic migration to add `tenant_id` column to `notes` table
  - Type: UUID
  - Foreign key to `tenants.id`
  - No database default (app handles the logic)
  - Set existing rows to default tenant: `00000000-0000-0000-0000-000000000000`
  - NOT NULL afer adding value to existing rows
- [x] Add index on `tenant_id` for query performance
- [x] Update `Note` model in `backend/models/note.py`:
  - Add `tenant_id` field with relationship to `Tenant`
- [x] Update `NoteCreate` schema to accept optional `tenant_id` (defaults to default tenant UUID in app logic)

**Testing**:
- [x] All existing tests pass (update as needed)

**User Impact**: None - all notes belong to default tenant, everything works as before

---

## Phase 2: Backend Tenant Logic (Still Using Default)

### Step 3: Add Tenant Service Layer ✅ COMPLETE
**Goal**: Create tenant management logic without changing API behavior

**Changes**:
- [x] Create `backend/services/tenant.py`:
  - `get_tenant_by_slug(slug)` - Look up tenant
  - `get_tenant_by_id(id)` - Get tenant by ID
  - `create_tenant(slug, name)` - Create new tenant
  - `list_tenants()` - Get all tenants
  - `update_tenant(slug, update_data)` - Update tenant
- [x] Create `backend/schemas/tenant.py`:
  - `TenantCreate` (slug, name)
  - `TenantRead` (id, slug, name, created_at, is_active)
  - `TenantUpdate` (name, is_active)
- [x] Add unit tests for tenant service (18 tests)
- [x] Add logging tests for tenant service (13 tests)
- [x] Add integration tests for tenant service (15 tests)

**Testing**:
- [x] All existing tests pass (87 tests total)
- [x] New tenant service tests pass
- [x] Can create, read, update, list tenants via service
- [x] Proper error handling (404, 409, 500)
- [x] Logging in place for all operations

**User Impact**: None - services exist but aren't used in API yet

---

### Step 4: Update Note Service to Filter by Tenant ✅ COMPLETE
**Goal**: Make note service tenant-aware, but still use default tenant

**Changes**:
- [x] Update `backend/services/note.py`:
  - Added `tenant_id` parameter to all methods (with DEFAULT_TENANT_ID as default)
  - `create_note(note_data, tenant_id)` - Create with tenant
  - `list_notes(tenant_id)` - Filter by tenant
  - `get_note_detail(note_id, tenant_id)` - Get specific note for tenant
  - `update_note(note_id, note_data, tenant_id)` - Update within tenant
  - `lock_note(note_id, tenant_id)` - Lock within tenant
  - `delete_note(note_id, tenant_id)` - Delete within tenant
- [x] All queries now filter by `tenant_id` using `.filter()` instead of `.filter_by()`
- [x] Updated all unit tests to use `.filter()` mock pattern
- [x] Updated all logging tests to use `.filter()` mock pattern
- [x] Added tenant isolation integration tests (3 tests)

**Testing**:
- [x] All existing tests pass (90 tests total: 18 note integration + 3 tenant isolation + 15 tenant integration + 13 note unit + 11 note logging + 18 tenant unit + 13 tenant logging)
- [x] Service properly isolates notes by tenant_id
- [x] All operations include tenant_id in logging
- [x] Can't access notes from different tenant (enforced at service layer)

**User Impact**: None - API still uses default tenant for everything (DEFAULT_TENANT_ID parameter)

---

## Phase 3: Tenant Context Middleware (Preparation)

### Step 5: Add Tenant Context Middleware (Default Tenant Only)
**Goal**: Extract tenant from path, but only support default tenant initially

**Changes**:
- [ ] Create `backend/api/middleware.py` tenant context middleware:
  - Extract path prefix (e.g., `/default/api/notes` → "default")
  - Lookup tenant by slug in database
  - Store tenant_id in `request.state.tenant_id`
  - If no tenant prefix, use default tenant
  - If invalid tenant, return 404
- [ ] Add middleware to FastAPI app
- [ ] Update all route dependencies to use `request.state.tenant_id`
- [ ] For now, only "default" tenant slug works

**Testing**:
- [ ] All existing tests pass (using `/default/...` or no prefix)
- [ ] Middleware extracts tenant correctly
- [ ] Invalid tenant returns 404
- [ ] `request.state.tenant_id` is set correctly

**User Impact**: Users must now use `/default/api/notes` (or backward compat with no prefix)
- Migration note: Update frontend to use `/default` prefix

---

## Phase 4: Multi-Tenant API Routes

### Step 6: Update API Routes for Tenant Path Prefix
**Goal**: All API routes work with tenant slug prefix

**Changes**:
- [ ] Update route definitions in `backend/api/main.py`:
  - Add optional tenant prefix: `/{tenant_slug}/api/notes`
  - Keep backward compat routes without prefix (use default)
- [ ] Update all note endpoints to use `request.state.tenant_id`
- [ ] Add tenant management endpoints (optional):
  - `POST /api/tenants` - Create tenant (admin only later)
  - `GET /api/tenants/{slug}` - Get tenant info
  - `GET /api/tenants/{slug}/available` - Check availability
- [ ] Update API error handling for tenant not found

**Testing**:
- [ ] Can access notes via `/default/api/notes`
- [ ] Can access notes via old route (backward compat)
- [ ] Create test tenant and verify isolation
- [ ] Notes from one tenant can't be accessed from another

**User Impact**: API now supports multiple tenants via path
- `/default/api/notes` - Default tenant
- `/tenant1/api/notes` - New tenant (once created)

---

## Phase 5: Frontend Multi-Tenant Support

### Step 7: Add Frontend Tenant Context
**Goal**: Frontend extracts and uses tenant from URL path

**Changes**:
- [ ] Update `src/App.js`:
  - Add React Router route: `/:tenantSlug/*`
  - Extract `tenantSlug` from params
  - Store in React Context or state
  - Pass tenant to all child components
- [ ] Update `src/config.js`:
  - Make API base URL tenant-aware: `/${tenantSlug}/api`
- [ ] Update `src/hooks/useNotes.js`:
  - Use tenant-aware API URLs
- [ ] Update all navigation links to include tenant slug

**Testing**:
- [ ] Can access app via `/default`
- [ ] All API calls include tenant in path
- [ ] Navigation maintains tenant context
- [ ] Direct navigation to tenant URL works

**User Impact**: Must access app via `http://localhost:3000/default`
- Old root URL redirects to `/default`

---

### Step 8: Tenant Directory & Management UI
**Goal**: Root page shows all tenants and allows creating new ones

**Changes**:
- [ ] Create `src/pages/TenantDirectory.js`:
  - Fetches all tenants from `GET /api/tenants`
  - Displays tenant cards in a grid (similar styling to notes page)
  - Each tenant card shows: name, slug, created date
  - Each tenant card is a link to `/{slug}` (enter that tenant's app)
  - "Create New Tenant" button at top
- [ ] Create `src/components/tenants/TenantCard.js`:
  - Card component for displaying tenant info
  - Click navigates to tenant's app
  - Styling matches note cards (Tailwind)
- [ ] Create `src/components/tenants/CreateTenantForm.js`:
  - Modal or inline form
  - Fields: name (required), slug (required, auto-generated from name)
  - Real-time slug availability check (debounced)
  - Validation feedback (slug format, availability, reserved words)
  - Submit creates tenant via `POST /api/tenants`
  - On success, navigate to new tenant or close modal
- [ ] Create `src/hooks/useTenants.js`:
  - `const { tenants, loading, error, createTenant, refetch } = useTenants()`
  - Fetches tenant list
  - Creates new tenant
  - Handles loading/error states
- [ ] Update `src/App.js`:
  - Add route: `"/"` → `<TenantDirectory />`
  - Keep route: `"/:tenantSlug/*"` → tenant app
  - Root now shows directory instead of redirecting

**Testing**:
- [ ] Root page (`/`) shows all existing tenants
- [ ] Can click tenant card to navigate to that tenant's app
- [ ] Can open create tenant form
- [ ] Slug auto-generates from name (e.g., "Acme Corp" → "acme-corp")
- [ ] Can manually edit slug
- [ ] Slug availability check works in real-time
- [ ] Invalid slugs show validation errors
- [ ] Can successfully create new tenant
- [ ] After creation, tenant appears in directory
- [ ] Can navigate into newly created tenant

**User Impact**: Root page is now a tenant directory/launcher
- `http://localhost:3000/` - Shows all tenants, create new
- `http://localhost:3000/default` - Default tenant's notes app
- `http://localhost:3000/tenant1` - Tenant1's notes app
- Easy self-service tenant creation

---

## Phase 6: Update Nginx for Path-Based Routing

### Step 9: Configure Nginx for Tenant Paths
**Goal**: Ensure Nginx correctly proxies tenant paths

**Changes**:
- [ ] Update `nginx/nginx.conf`:
  - Ensure proxy passes preserve full path
  - Handle tenant-prefixed routes
  - Verify API and frontend routes work with tenant prefix
- [ ] Test all routes through Nginx

**Testing**:
- [ ] Access via Nginx: `http://localhost/default`
- [ ] API calls work: `http://localhost/default/api/notes`
- [ ] Static assets load correctly

**User Impact**: Works via Nginx proxy (production-like setup)

---

## Phase 7: Testing & Data Seeding

### Step 10: Comprehensive Testing & Seed Data
**Goal**: Full test coverage and realistic seed data

**Changes**:
- [ ] Update `backend/tests/conftest.py`:
  - Add tenant fixtures
  - Create multi-tenant test data
- [ ] Update integration tests in `backend/tests/integration/`:
  - Test tenant isolation
  - Test cross-tenant access prevention
  - Test invalid tenant handling
- [ ] Create seed script for development:
  - Multiple tenants with sample notes
  - Easy reset/reseed command
- [ ] Update service tests to cover tenant scenarios

**Testing**:
- [ ] All test suites pass
- [ ] 100% of tenant isolation scenarios covered
- [ ] Can't access notes from wrong tenant
- [ ] Can't update/delete notes from wrong tenant

**User Impact**: Confidence that multi-tenancy is secure and working

---

## Phase 8: Documentation & Cleanup

### Step 11: Documentation & Developer Experience
**Goal**: Make it easy for developers to understand and use

**Changes**:
- [ ] Update README with:
  - Multi-tenancy architecture explanation
  - How to create new tenants
  - URL structure documentation
  - Development workflow with tenants
- [ ] Add migration guide for existing users
- [ ] Document tenant management
- [ ] Add inline code comments for tenant logic

**Testing**:
- [ ] Follow README instructions on fresh checkout
- [ ] Verify all steps work as documented

**User Impact**: Clear understanding of how to work with tenants

---

## Future Enhancements (Not in Initial Implementation)

- [ ] Add Row-Level Security (RLS) policies for defense in depth
- [ ] Add tenant admin users and permissions
- [ ] Add tenant settings/configuration
- [ ] Add tenant usage metrics
- [ ] Add tenant-specific feature flags
- [ ] Add soft delete for tenants
- [ ] Add tenant onboarding flow with signup
- [ ] Add custom domains per tenant (advanced)
- [ ] Add subdomain routing option

---

## Rollback Plan

Each step can be rolled back independently:
1. Revert git commit
2. Run previous migration: `alembic downgrade -1`
3. Restart services

---

## Testing Strategy Per Step

For each step:
1. Run all existing tests: `pytest`
2. Run new tests for the feature
3. Manual smoke test of API endpoints
4. Verify frontend still works
5. Check database state with `psql` or pgAdmin

---

## Notes

- **Default tenant UUID**: `00000000-0000-0000-0000-000000000000`
- **Default tenant slug**: `default`
- **Test tenant slugs**: `tenant1`, `tenant2`, `demo`
- **Backward compatibility**: Maintain for at least 2 steps before removing
