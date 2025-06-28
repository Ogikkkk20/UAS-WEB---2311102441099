# AJAX Upload Implementation Guide

## Overview

Upload video dan image sekarang berjalan di belakang layar (background) menggunakan AJAX untuk mencegah blocking UI saat upload file besar.

## Features Implemented

### 1. Background Video Upload

- **File Size Limit**: 500MB
- **Supported Formats**: MP4, AVI, MOV, WMV, FLV
- **Progress Bar**: Real-time upload progress dengan persentase
- **Preview**: Menampilkan informasi file setelah upload berhasil
- **Validation**: Validasi ukuran dan tipe file

### 2. Background Image Upload (Poster)

- **File Size Limit**: 10MB
- **Supported Formats**: JPEG, JPG, PNG, GIF, WebP
- **Loading State**: Spinner saat uploading
- **Preview**: Menampilkan preview image setelah upload
- **Drag & Drop**: Support drag and drop file

### 3. Form Protection

- **Upload State Tracking**: Mencegah submit form saat upload sedang berjalan
- **Button State**: Button disabled dengan visual feedback saat uploading
- **Notification System**: Toast notifications untuk success/error

## Technical Implementation

### Backend (Django)

#### Views (`films/views.py`)

```python
# AJAX Upload Endpoints
@login_required
@user_passes_test(is_staff_user)
@require_POST
def upload_video_ajax(request):
    # Handles video upload with validation

@login_required
@user_passes_test(is_staff_user)
@require_POST
def upload_image_ajax(request):
    # Handles image upload with validation
```

#### URLs (`films/urls.py`)

```python
# AJAX Upload URLs
path('ajax/upload-video/', views.upload_video_ajax, name='upload_video_ajax'),
path('ajax/upload-image/', views.upload_image_ajax, name='upload_image_ajax'),
```

#### Forms (`films/forms.py`)

```python
class FilmForm(forms.ModelForm):
    # Hidden fields for AJAX uploaded files
    video_path = forms.CharField(required=False, widget=forms.HiddenInput())
    poster_path = forms.CharField(required=False, widget=forms.HiddenInput())
```

### Frontend (JavaScript)

#### Upload Functions (`static/js/modern-dashboard.js`)

- `uploadVideoFile(file)`: Handles video upload with progress tracking
- `uploadPosterFile(file)`: Handles image upload
- `initializeFileUploads()`: Sets up drag & drop and click handlers
- Upload state management dengan `window.uploadState`

#### Template Integration (`templates/dashboard/modern_film_form.html`)

- Alpine.js untuk reactive form state
- Progress bars dan preview elements
- Form submission protection
- CKEditor integration tetap utuh

## How It Works

### Video Upload Process:

1. User selects/drops video file
2. JavaScript validates file size and type
3. AJAX request dimulai dengan progress tracking
4. Server menyimpan file ke lokasi temporary
5. Progress bar update real-time
6. Setelah selesai, preview ditampilkan
7. Hidden input diisi dengan file path
8. Form bisa di-submit dengan file path

### Image Upload Process:

1. User selects/drops image file
2. JavaScript validates file
3. AJAX request dengan loading spinner
4. Server menyimpan file temporary
5. Preview image ditampilkan
6. Hidden input diisi dengan file path

### Form Submission:

1. Form checks jika ada upload yang sedang berjalan
2. Jika ada upload aktif, submit dicegah dengan notification
3. Jika tidak ada upload, form submit normal
4. Server memindahkan file dari temporary ke permanent location

## User Experience Improvements

### Before (Traditional Upload):

- ❌ Form blocks saat upload file besar
- ❌ No progress feedback
- ❌ Page refresh pada error
- ❌ User harus tunggu upload selesai

### After (AJAX Upload):

- ✅ Upload berjalan di background
- ✅ Real-time progress bar
- ✅ Instant feedback dan preview
- ✅ Form tetap responsive
- ✅ Better error handling
- ✅ Drag & drop support

## File Structure

```
static/js/modern-dashboard.js
├── initializeFileUploads()
├── uploadVideoFile()
├── uploadPosterFile()
├── progress tracking
└── state management

templates/dashboard/modern_film_form.html
├── Upload areas dengan drag & drop
├── Progress bars
├── Preview elements
└── Alpine.js form protection

films/views.py
├── upload_video_ajax()
├── upload_image_ajax()
├── film_create() - handles AJAX files
└── film_edit() - handles AJAX files
```

## Usage Instructions

1. **Drag & Drop**: Seret file ke area upload
2. **Click Upload**: Klik area upload untuk buka file dialog
3. **Progress Monitoring**: Lihat progress bar untuk video upload
4. **Preview**: File preview muncul otomatis setelah upload
5. **Form Submit**: Submit form normal setelah upload selesai

## Error Handling

- File size validation
- File type validation
- Network error handling
- Server error feedback
- Upload state cleanup
- User-friendly notifications

## Testing Scenarios

1. ✅ Upload video file kecil (< 100MB)
2. ✅ Upload video file besar (> 100MB, < 500MB)
3. ✅ Upload file melebihi limit (> 500MB)
4. ✅ Upload file format tidak didukung
5. ✅ Network error simulation
6. ✅ Multiple file upload scenario
7. ✅ Form submit saat upload berjalan
8. ✅ Drag & drop functionality

Implementasi AJAX upload ini memberikan user experience yang jauh lebih baik dengan upload yang tidak memblokir interface dan feedback yang real-time.
