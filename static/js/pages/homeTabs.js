const HomeTab = document.querySelector('#mainTab');
const tabs = HomeTab.querySelectorAll('button[data-bs-toggle="tab"]');

tabs.forEach(tab => {
    tab.addEventListener('shown.bs.tab', (event) => {
        const { target } = event;
        const { id: targetId } = target;
        
        saveTabId('activeHomeTabId',targetId);
    });
});

const saveTabId = (location, selector) => {
    localStorage.setItem(location, selector);
};

const getTabId = () => {
    const activeHomeTabId = localStorage.getItem('activeHomeTabId');

    // if local storage item is null, show default tab
    if (!activeHomeTabId) return;

    // call 'show' function
    if (activeHomeTabId) {
        const someTabHomeTrigger = document.querySelector(`#${activeHomeTabId}`)
        const tab = new bootstrap.Tab(someTabHomeTrigger);
        tab.show();
    }
};

// get pill id on load
getTabId();