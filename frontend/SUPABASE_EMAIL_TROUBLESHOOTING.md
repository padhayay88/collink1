# Supabase Email Troubleshooting Guide

## 🔍 **Common Issues & Solutions**

### **1. SMTP Configuration Issues**

**Check your SMTP settings in Supabase:**
- Go to Authentication → Settings → SMTP Settings
- Verify all fields are correct:
  - SMTP Host (e.g., smtp.gmail.com)
  - SMTP Port (587 for TLS, 465 for SSL)
  - SMTP User (your email)
  - SMTP Pass (your app password)
  - Sender Name (Collink)
  - Sender Email (must be verified)

**Common SMTP Providers:**
```
Gmail:
- Host: smtp.gmail.com
- Port: 587
- Use App Password (not regular password)

Outlook/Hotmail:
- Host: smtp-mail.outlook.com
- Port: 587

Yahoo:
- Host: smtp.mail.yahoo.com
- Port: 587
```

### **2. Email Confirmation Settings**

**In Supabase Dashboard:**
- Authentication → Settings → General
- ✅ Enable email confirmations
- ✅ Set Site URL to: `http://localhost:3000`
- ✅ Add Redirect URLs:
  - `http://localhost:3000/auth/callback`
  - `http://localhost:3000/register`

### **3. Email Template Issues**

**Check Email Templates:**
- Authentication → Settings → Email Templates
- Verify "Confirm signup" template is active
- Check template content for any errors

### **4. Project Status**

**Verify Project is Active:**
- Check if your Supabase project is paused
- Ensure you haven't exceeded usage limits
- Verify project is in the correct region

## 🧪 **Testing Steps**

### **Step 1: Test SMTP Connection**
1. Go to `http://localhost:3000/test-supabase`
2. Enter a real email address
3. Check browser console for errors
4. Look for any error messages

### **Step 2: Check Supabase Logs**
1. Go to your Supabase dashboard
2. Check Logs → Auth logs
3. Look for any email sending errors

### **Step 3: Test with Different Email**
- Try with a different email provider
- Check spam/junk folders
- Verify email address is correct

## 🚀 **Alternative Solutions**

### **Option 1: Use Supabase's Default Email Service**
- Disable custom SMTP
- Use Supabase's built-in email service
- This often works better for testing

### **Option 2: Disable Email Confirmation**
- Temporarily disable email confirmations
- Users can register without email verification
- Enable later when SMTP is working

### **Option 3: Use Local Authentication**
- The fallback system already works
- Users can register and use auth codes
- No email dependency

## 🔧 **Quick Fixes**

### **For Gmail SMTP:**
1. Enable 2-factor authentication
2. Generate an App Password
3. Use App Password in SMTP settings

### **For Outlook/Hotmail:**
1. Enable "Less secure app access"
2. Or use App Password

### **For Yahoo:**
1. Enable "Allow apps that use less secure sign in"
2. Or generate App Password

## 📧 **Email Verification Flow**

The current system has a fallback:
1. Try Supabase email verification
2. If email fails, show auth code input
3. User can verify with 6-digit code
4. Account is created and user is logged in

This ensures registration works even if email fails!
