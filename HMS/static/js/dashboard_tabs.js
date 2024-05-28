const tabs = document.querySelectorAll('.tab');
const tabContents = document.querySelectorAll('.tab-content');

tabs.forEach((tab, index) => {
  tab.addEventListener('click', () => {
    tabs.forEach((t) => t.classList.remove('tab-active'));
    tab.classList.add('tab-active');

    tabContents.forEach((tc) => tc.classList.add('hidden'));
    tabContents[index].classList.remove('hidden');
  });
});