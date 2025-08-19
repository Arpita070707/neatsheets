// Cleaner CSV App - Main JavaScript File

class CSVCleanerApp {
    constructor() {
        this.currentSessionId = null;
        this.cleaningHistory = [];
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // File upload form
        document.getElementById('uploadForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleFileUpload();
        });

        // Reset button
        document.getElementById('resetBtn').addEventListener('click', () => {
            this.resetDataset();
        });

        // Download button
        document.getElementById('downloadBtn').addEventListener('click', () => {
            this.downloadCleanedCSV();
        });
    }

    async handleFileUpload() {
        const fileInput = document.getElementById('csvFile');
        const file = fileInput.files[0];

        if (!file) {
            this.showError('Please select a CSV file');
            return;
        }

        if (!file.name.endsWith('.csv')) {
            this.showError('Please select a valid CSV file');
            return;
        }

        this.showLoading(true);
        
        const formData = new FormData();
        formData.append('csv_file', file);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                this.currentSessionId = data.session_id;
                this.displayDatasetSummary(data.summary);
                this.showCleaningOperations();
                this.showControlButtons();
                this.clearResults();
                this.showSuccess('CSV file uploaded successfully!');
            } else {
                this.showError(data.error || 'Failed to upload file');
            }
        } catch (error) {
            this.showError('Network error: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }

    async performCleaning(operation, method = null, threshold = null) {
        if (!this.currentSessionId) {
            this.showError('No dataset loaded. Please upload a CSV file first.');
            return;
        }

        this.showLoading(true);

        const requestData = {
            operation: operation
        };

        if (method) {
            requestData.method = method;
        }

        if (threshold !== null) {
            requestData.threshold = threshold;
        }

        try {
            const response = await fetch('/api/clean', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            });

            const data = await response.json();

            if (data.success) {
                this.addCleaningResult(data.result);
                this.updateDatasetSummary(data.result.after_summary);
                this.showSuccess(`Operation completed: ${data.result.operation}`);
            } else {
                this.showError(data.error || 'Cleaning operation failed');
            }
        } catch (error) {
            this.showError('Network error: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }

    async resetDataset() {
        if (!this.currentSessionId) {
            return;
        }

        try {
            const response = await fetch('/api/reset', {
                method: 'POST'
            });

            const data = await response.json();

            if (data.success) {
                this.cleaningHistory = [];
                this.clearResults();
                this.displayDatasetSummary(data.summary);
                this.showSuccess('Dataset reset to original state');
            } else {
                this.showError(data.error || 'Failed to reset dataset');
            }
        } catch (error) {
            this.showError('Network error: ' + error.message);
        }
    }

    async downloadCleanedCSV() {
        if (!this.currentSessionId) {
            this.showError('No dataset loaded');
            return;
        }

        try {
            const response = await fetch('/api/download', {
                method: 'POST'
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'cleaned_dataset.csv';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                this.showSuccess('Download started!');
            } else {
                const data = await response.json();
                this.showError(data.error || 'Download failed');
            }
        } catch (error) {
            this.showError('Network error: ' + error.message);
        }
    }

    displayDatasetSummary(summary) {
        const summaryDiv = document.getElementById('summaryContent');
        
        summaryDiv.innerHTML = `
            <div class="summary-item">
                <div class="summary-value">${summary.rows.toLocaleString()}</div>
                <div class="summary-label">Rows</div>
            </div>
            <div class="summary-item">
                <div class="summary-value">${summary.columns}</div>
                <div class="summary-label">Columns</div>
            </div>
            <div class="summary-item">
                <div class="summary-value">${summary.total_missing.toLocaleString()}</div>
                <div class="summary-label">Missing Values</div>
            </div>
            <div class="summary-item">
                <div class="summary-value">${summary.duplicates.toLocaleString()}</div>
                <div class="summary-label">Duplicates</div>
            </div>
            <div class="summary-item">
                <div class="summary-value">${summary.column_names.length}</div>
                <div class="summary-label">Unique Columns</div>
            </div>
        `;

        document.getElementById('datasetSummary').style.display = 'block';
    }

    updateDatasetSummary(summary) {
        this.displayDatasetSummary(summary);
    }

    addCleaningResult(result) {
        this.cleaningHistory.push(result);
        this.displayCleaningResult(result);
    }

    displayCleaningResult(result) {
        const resultsContainer = document.getElementById('resultsContainer');
        
        const operationResult = document.createElement('div');
        operationResult.className = 'operation-result';
        
        const iconClass = this.getOperationIcon(result.operation);
        const iconBg = this.getOperationIconBg(result.operation);
        
        operationResult.innerHTML = `
            <div class="operation-header">
                <div class="operation-icon ${iconBg}">
                    <i class="bi ${iconClass}"></i>
                </div>
                <h5 class="operation-title">${result.operation}</h5>
            </div>
            
            <p class="operation-description">${result.description}</p>
            
            <div class="comparison-container">
                <div class="comparison-card before">
                    <h6>Before Operation</h6>
                    ${this.createSummaryStats(result.before_summary)}
                </div>
                <div class="comparison-card after">
                    <h6>After Operation</h6>
                    ${this.createSummaryStats(result.after_summary)}
                </div>
            </div>
        `;
        
        resultsContainer.appendChild(operationResult);
        
        // Scroll to the new result
        operationResult.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    createSummaryStats(summary) {
        return `
            <div class="stat-item">
                <span class="stat-label">Rows:</span>
                <span class="stat-value">${summary.rows.toLocaleString()}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Columns:</span>
                <span class="stat-value">${summary.columns}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Missing Values:</span>
                <span class="stat-value">${summary.total_missing.toLocaleString()}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Duplicates:</span>
                <span class="stat-value">${summary.duplicates.toLocaleString()}</span>
            </div>
        `;
    }

    getOperationIcon(operation) {
        const iconMap = {
            'Remove Duplicates': 'bi-trash',
            'Fill Missing Values': 'bi-funnel',
            'Drop High Missing Columns': 'bi-columns-gap',
            'Remove Special Characters': 'bi-textarea-t',
            'Convert Data Types': 'bi-arrow-repeat'
        };
        
        return iconMap[operation] || 'bi-gear';
    }

    getOperationIconBg(operation) {
        const bgMap = {
            'Remove Duplicates': 'bg-danger',
            'Fill Missing Values': 'bg-info',
            'Drop High Missing Columns': 'bg-warning',
            'Remove Special Characters': 'bg-secondary',
            'Convert Data Types': 'bg-primary'
        };
        
        return bgMap[operation] || 'bg-secondary';
    }

    showCleaningOperations() {
        document.getElementById('cleaningOperations').style.display = 'block';
    }

    showControlButtons() {
        document.getElementById('controlButtons').style.display = 'flex';
    }

    clearResults() {
        const resultsContainer = document.getElementById('resultsContainer');
        resultsContainer.innerHTML = '';
    }

    showLoading(show) {
        const loadingIndicator = document.getElementById('loadingIndicator');
        
        if (show) {
            loadingIndicator.style.display = 'flex';
        } else {
            loadingIndicator.style.display = 'none';
        }
    }

    showSuccess(message) {
        this.showMessage(message, 'success');
    }

    showError(message) {
        this.showMessage(message, 'error');
    }

    showMessage(message, type) {
        // Remove existing messages
        const existingMessages = document.querySelectorAll('.success-message, .error-message');
        existingMessages.forEach(msg => msg.remove());

        const messageDiv = document.createElement('div');
        messageDiv.className = type === 'success' ? 'success-message' : 'error-message';
        messageDiv.textContent = message;

        // Insert at the top of the results container
        const resultsContainer = document.getElementById('resultsContainer');
        if (resultsContainer.firstChild) {
            resultsContainer.insertBefore(messageDiv, resultsContainer.firstChild);
        } else {
            resultsContainer.appendChild(messageDiv);
        }

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (messageDiv.parentNode) {
                messageDiv.remove();
            }
        }, 5000);
    }
}

// Global function for cleaning operations (called from HTML onclick)
function performCleaning(operation, method = null, threshold = null) {
    app.performCleaning(operation, method, threshold);
}

// Initialize the app when the page loads
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new CSVCleanerApp();
});
