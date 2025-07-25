# Libsys

## Membership System

The library implements a membership system with three different membership types:

### Membership Types

1. **Basic Membership**
   - Monthly Fee: $5.00
   - Annual Fee: $50.00
   - Maximum Books: 3 books at a time
   - Loan Period: 14 days
   - Extensions: Not available

2. **Premium Membership**
   - Monthly Fee: $10.00
   - Annual Fee: $100.00
   - Maximum Books: 5 books at a time
   - Loan Period: 14 days
   - Extensions: Can request 7-day extensions (requires librarian approval)

3. **Student Membership**
   - Monthly Fee: $3.00
   - Annual Fee: $30.00
   - Maximum Books: 4 books at a time
   - Loan Period: 21 days
   - Extensions: Not available

### Setting Up Membership Types

To create the default membership types, run:

```bash
python manage.py create_membership_types
```

### Assigning Memberships

Memberships can be assigned to users through the Django admin interface. Users without a membership cannot borrow books.
