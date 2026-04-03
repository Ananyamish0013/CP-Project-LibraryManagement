const API_BASE = 'http://127.0.0.1:5000/api';

const api = {
    async getBooks(search = '') {
        const url = search ? `${API_BASE}/books?search=${encodeURIComponent(search)}` : `${API_BASE}/books`;
        const res = await fetch(url);
        if (!res.ok) throw new Error('Failed to fetch books');
        return res.json();
    },

    async addBook(bookData) {
        const res = await fetch(`${API_BASE}/books`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(bookData)
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Failed to add book');
        return data;
    },

    async deleteBook(id) {
        const res = await fetch(`${API_BASE}/books/${id}`, { method: 'DELETE' });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Failed to delete book');
        return data;
    },

    async getUsers() {
        const res = await fetch(`${API_BASE}/users`);
        if (!res.ok) throw new Error('Failed to fetch users');
        return res.json();
    },

    async addUser(userData) {
        const res = await fetch(`${API_BASE}/users`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData)
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Failed to add user');
        return data;
    },

    async issueBook(issueData) {
        const res = await fetch(`${API_BASE}/issue`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(issueData)
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Failed to issue book');
        return data;
    },

    async returnBook(returnData) {
        const res = await fetch(`${API_BASE}/return`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(returnData)
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Failed to return book');
        return data;
    }
};

function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container') || createToastContainer();
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
    return container;
}
