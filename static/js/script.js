class GestureAI {
    constructor() {
        this.isCameraActive = false;
        this.updateInterval = null;
        
        // DOM Elements
        this.videoFeed = document.getElementById('videoFeed');
        this.startBtn = document.getElementById('startCamera');
        this.stopBtn = document.getElementById('stopCamera');
        this.cameraStatus = document.getElementById('cameraStatus');
        this.statusText = document.getElementById('statusText');
        this.detectedGesture = document.getElementById('detectedGesture');
        this.detectedAction = document.getElementById('detectedAction');
        this.videoPlaceholder = document.getElementById('videoPlaceholder');
        
        this.init();
    }
    
    init() {
        this.startBtn.addEventListener('click', () => this.startCamera());
        this.stopBtn.addEventListener('click', () => this.stopCamera());
    }
    
    async startCamera() {
        try {
            this.startBtn.disabled = true;
            this.startBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            this.statusText.textContent = 'Starting...';
            
            const response = await fetch('/start_camera', { 
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.isCameraActive = true;
                
                // Simple video feed - no timestamp to avoid caching issues
                this.videoFeed.src = '/video_feed';
                this.videoFeed.style.display = 'block';
                this.videoPlaceholder.style.display = 'none';
                
                // Update UI
                this.startBtn.disabled = false;
                this.stopBtn.disabled = false;
                this.cameraStatus.classList.add('active');
                this.statusText.textContent = 'Camera Online';
                this.startBtn.innerHTML = '<i class="fas fa-play"></i>';
                
                // Start polling for gestures
                this.startPolling();
                
                this.showToast('Camera started!', 'success');
            } else {
                throw new Error(data.message);
            }
        } catch (error) {
            console.error(error);
            this.startBtn.disabled = false;
            this.startBtn.innerHTML = '<i class="fas fa-play"></i>';
            this.statusText.textContent = 'Camera Offline';
            this.showToast('Failed to start camera', 'error');
        }
    }
    
    async stopCamera() {
        try {
            await fetch('/stop_camera', { method: 'POST' });
            
            this.isCameraActive = false;
            this.videoFeed.src = '';
            this.videoFeed.style.display = 'none';
            this.videoPlaceholder.style.display = 'flex';
            
            this.startBtn.disabled = false;
            this.stopBtn.disabled = true;
            this.cameraStatus.classList.remove('active');
            this.statusText.textContent = 'Camera Offline';
            
            if (this.updateInterval) {
                clearInterval(this.updateInterval);
                this.updateInterval = null;
            }
            
            this.showToast('Camera stopped', 'info');
        } catch (error) {
            console.error(error);
        }
    }
    
    startPolling() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }
        
        this.updateInterval = setInterval(async () => {
            if (!this.isCameraActive) return;
            
            try {
                const response = await fetch('/capture_frame', { 
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });
                
                const data = await response.json();
                
                if (data.success && data.gesture_results?.stable_gesture) {
                    const g = data.gesture_results.stable_gesture;
                    this.detectedGesture.textContent = `${g.emoji} ${g.name}`;
                    this.detectedAction.textContent = g.action;
                }
            } catch (error) {
                console.error('Polling error:', error);
            }
        }, 500);
    }
    
    showToast(message, type) {
        const toast = document.createElement('div');
        toast.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: ${type === 'success' ? '#00b894' : type === 'error' ? '#d63031' : '#0984e3'};
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            z-index: 9999;
            animation: slideIn 0.3s;
        `;
        toast.textContent = message;
        document.body.appendChild(toast);
        
        setTimeout(() => toast.remove(), 3000);
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    window.gestureAI = new GestureAI();
});