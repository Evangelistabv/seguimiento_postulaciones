const menuButton = document.querySelector('.menu-button');
const sidebar = document.querySelector('.sidebar');
menuButton?.addEventListener('click', () => sidebar?.classList.toggle('open'));

const activityToggle = document.querySelector('[data-toggle="activity-form"]');
const activityForm = document.querySelector('#activity-form');
activityToggle?.addEventListener('click', () => {
  activityForm?.classList.toggle('visible');
  activityForm?.querySelector('input, select, textarea')?.focus();
});

setTimeout(() => document.querySelector('.toast')?.classList.add('hide'), 3200);
