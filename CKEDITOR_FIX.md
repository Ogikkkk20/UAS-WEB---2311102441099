# Fix untuk Error "Invalid form control not focusable"

## Problem

Error: `An invalid form control with name='description' is not focusable`

## Root Cause

- CKEditor menggantikan textarea asli dengan editor yang kompleks
- HTML5 form validation masih mencoba fokus ke textarea asli yang sudah tersembunyi
- Textarea memiliki `required` attribute tetapi tidak dapat difokus setelah CKEditor diinisialisasi

## Solution Implemented

### 1. **Disable HTML5 Validation**

```html
<form method="post" ... novalidate></form>
```

- Menambahkan `novalidate` attribute pada form
- Mencegah browser native validation yang conflict dengan CKEditor

### 2. **Remove Required Attribute from CKEditor Textareas**

```html
<!-- Before -->
<textarea id="description-editor" name="description" required>

<!-- After -->
<textarea id="description-editor" name="description">
```

- Menghapus `required` dari textarea yang akan digantikan CKEditor
- Mencegah conflict antara HTML5 validation dan CKEditor

### 3. **Custom JavaScript Validation**

```javascript
validateForm() {
    let isValid = true;

    // Validate regular fields
    const title = document.querySelector('input[name="title"]').value.trim();
    if (!title) {
        errors.push('Title is required');
        isValid = false;
    }

    // Validate CKEditor content
    if (this.editors.description) {
        const content = this.editors.description.getData().trim();
        if (!content || content === '<p>&nbsp;</p>') {
            // Show custom error message
            isValid = false;
        }
    }

    return isValid;
}
```

### 4. **Improved Form Submission Handling**

```javascript
handleFormSubmit(event) {
    // Check upload state
    if (this.uploading) {
        event.preventDefault();
        return false;
    }

    // Custom validation
    if (!this.validateForm()) {
        event.preventDefault();
        showNotification('Please fill in all required fields', 'error');
        return false;
    }

    // Update all CKEditor content before submit
    if (this.editors.description) {
        document.querySelector('#description-editor').value = this.editors.description.getData();
    }

    return true;
}
```

### 5. **Store CKEditor References**

```javascript
// Store editor references in Alpine.js component
formComponent._x_dataStack[0].editors.description = editor;
formComponent._x_dataStack[0].editors.synopsis = editor;
formComponent._x_dataStack[0].editors.cast = editor;
```

### 6. **Real-time Error Clearing**

```javascript
// Clear error when user starts typing in CKEditor
editor.model.document.on("change:data", () => {
  const descriptionError = document.getElementById("description-error");
  if (descriptionError) {
    descriptionError.classList.add("hidden");
  }
});
```

## Changes Made

### Template (`templates/dashboard/modern_film_form.html`):

1. ✅ Added `novalidate` to form
2. ✅ Removed `required` from description textarea
3. ✅ Added custom error message container
4. ✅ Improved Alpine.js form handling
5. ✅ Enhanced CKEditor initialization
6. ✅ Custom validation logic

### Benefits:

- ✅ **No more "not focusable" errors**
- ✅ **Better user experience** with custom validation
- ✅ **Real-time error feedback**
- ✅ **Consistent validation** across all fields
- ✅ **CKEditor integration** works seamlessly
- ✅ **Upload state protection** maintained

## Testing:

1. **Try submitting empty form** → Custom validation should show errors
2. **Fill description in CKEditor** → Error should clear automatically
3. **Submit with all fields** → Should work without errors
4. **Upload files during editing** → Form should prevent submission until upload complete

## Result:

Form sekarang menggunakan custom validation yang bekerja dengan CKEditor tanpa conflict dengan HTML5 validation. Error "invalid form control not focusable" sudah teratasi! 🎯
