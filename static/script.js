document.addEventListener('DOMContentLoaded', () => {
    const tasks = document.querySelectorAll('.task-card');
    tasks.forEach(task => {
        task.addEventListener('mouseenter', () => {
            task.style.transform = 'scale(1.02)';
            task.style.boxShadow = '0 6px 12px rgba(0, 0, 0, 0.1)';
        });

        task.addEventListener('mouseleave', () => {
            task.style.transform = 'scale(1)';
            task.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.05)';
        });
    });
});