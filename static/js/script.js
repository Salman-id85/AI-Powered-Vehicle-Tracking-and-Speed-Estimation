document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('uploadArea');
    const videoInput = document.getElementById('videoInput');
    const uploadButton = document.getElementById('uploadButton');
    const fileInfo = document.getElementById('statusMessage');
    const queryButton = document.getElementById('queryButton');
    const closeButtons = document.querySelectorAll('.status-message .btn-close');
  
    // Hamburger Menu Toggle
    document.querySelector('.hamburger').addEventListener('click', () => {
      document.querySelector('nav ul').classList.toggle('active');
    });
  
    // Header scroll effect
    window.addEventListener('scroll', () => {
      const header = document.querySelector('header');
      if (window.scrollY > 50) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    });
  
    // Scroll Animation for Stats and Image
    let ticking = false;
    window.addEventListener('scroll', () => {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          const stats = document.querySelectorAll('.stat');
          const image = document.querySelector('.reveal-img');
          const triggerBottom = window.innerHeight * 0.85;
  
          stats.forEach(stat => {
            const boxTop = stat.getBoundingClientRect().top;
            if (boxTop < triggerBottom) stat.classList.add('active');
          });
  
          if (image && image.getBoundingClientRect().top < triggerBottom) {
            image.classList.add('active');
          }
  
          ticking = false;
        });
        ticking = true;
      }
    });
  
    // Contact Form Submission
    document.getElementById('contactForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(e.target);
      try {
        const response = await fetch('/contact', {
          method: 'POST',
          body: formData
        });
        if (response.ok) {
          showSuccess('Thank you for your message! We will get back to you soon.');
          e.target.reset();
        } else {
          showError('Failed to send message. Please try again.');
        }
      } catch (err) {
        showError('Error: ' + err.message);
      }
    });
  
    // Drag-and-Drop Handling
    if (dropZone) {
      dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('active');
      });
  
      dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('active');
      });
  
      dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('active');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
          videoInput.files = files;
          fileInfo.textContent = `Selected: ${files[0].name}`;
          fileInfo.className = 'status-message success';
        }
      });
  
      dropZone.addEventListener('click', () => {
        videoInput.click();
      });
  
      videoInput.addEventListener('change', () => {
        if (videoInput.files.length > 0) {
          fileInfo.textContent = `Selected: ${videoInput.files[0].name}`;
          fileInfo.className = 'status-message success';
        } else {
          fileInfo.textContent = 'No file selected';
          fileInfo.className = 'status-message';
        }
      });
    }
  
    // Upload Handling
    if (uploadButton) {
      uploadButton.addEventListener('click', async (e) => {
        e.preventDefault();
        const file = videoInput.files[0];
        if (!file) {
          showError('Please select a video file.');
          return;
        }
        if (!file.type.startsWith('video/')) {
          showError('Please upload a valid video file (mp4, avi, mov).');
          return;
        }
  
        const formData = new FormData();
        formData.append('video', file);
  
        uploadButton.disabled = true;
        uploadButton.textContent = 'Processing...';
  
        try {
          const response = await fetch('/', {
            method: 'POST',
            body: formData
          });
  
          if (!response.ok) {
            const error = await response.text();
            showError('Upload failed: ' + error);
            uploadButton.disabled = false;
            uploadButton.textContent = 'Upload Video';
            return;
          }
  
          window.location.href = '/results';
        } catch (err) {
          showError('Upload error: ' + err.message);
          uploadButton.disabled = false;
          uploadButton.textContent = 'Upload Video';
        }
      });
    }
  
    // Search Functionality
    if (queryButton) {
      queryButton.addEventListener('click', async (e) => {
        e.preventDefault();
        const trackerId = document.getElementById('trackerId').value;
        if (!trackerId || isNaN(trackerId)) {
          showError('Please enter a valid numeric Tracker ID.');
          return;
        }
  
        const formData = new FormData();
        formData.append('tracker_id', trackerId);
  
        queryButton.disabled = true;
        queryButton.textContent = 'Searching...';
  
        try {
          const response = await fetch('/results', {
            method: 'POST',
            body: formData
          });
  
          if (!response.ok) {
            const error = await response.text();
            showError('Search failed: ' + error);
            queryButton.disabled = false;
            queryButton.textContent = 'Search';
            return;
          }
  
          window.location.reload();
        } catch (err) {
          showError('Search error: ' + err.message);
          queryButton.disabled = false;
          queryButton.textContent = 'Search';
        }
      });
    }
  
    // Close Flash Messages
    closeButtons.forEach(button => {
      button.addEventListener('click', () => {
        button.parentElement.remove();
      });
    });
  
    // Error Display Function
    function showError(message) {
      fileInfo.textContent = message;
      fileInfo.className = 'status-message error';
      fileInfo.style.display = 'block';
    }
  
    // Success Display Function
    function showSuccess(message) {
      fileInfo.textContent = message;
      fileInfo.className = 'status-message success';
      fileInfo.style.display = 'block';
    }
  });