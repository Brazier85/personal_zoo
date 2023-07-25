const TerrariumTab = document.querySelector('#settingsTerrariumTab');
const animalTab = document.querySelector('#settingsAnimalTab');
const t_tabs = TerrariumTab.querySelectorAll('button[data-bs-toggle="tab"]');
const a_tabs = animalTab.querySelectorAll('button[data-bs-toggle="tab"]');

t_tabs.forEach(tab => {
    tab.addEventListener('shown.bs.tab', (event) => {
        const { target } = event;
        const { id: targetId } = target;
        
        saveTabId('activeAnimalTabId',targetId);
    });
});

a_tabs.forEach(tab => {
    tab.addEventListener('shown.bs.tab', (event) => {
        const { target } = event;
        const { id: targetId } = target;
        
        saveTabId('activeTerrariumTabId',targetId);
    });
});

const saveTabId = (location, selector) => {
    localStorage.setItem(location, selector);
};

const getTabId = () => {
    const activeAnimalTabId = localStorage.getItem('activeAnimalTabId');
    const activeTerrariumTabId = localStorage.getItem('activeTerrariumTabId');

    // if local storage item is null, show default tab
    if (!activeAnimalTabId && !activeTerrariumTabId) return;

    // call 'show' function
    if (activeAnimalTabId) {
        const someTabAnimalTrigger = document.querySelector(`#${activeAnimalTabId}`)
        const tab = new bootstrap.Tab(someTabAnimalTrigger);
        tab.show();
    }

    if (activeTerrariumTabId) {
        const someTabTerrariumTrigger = document.querySelector(`#${activeTerrariumTabId}`)
        let tab = new bootstrap.Tab(someTabTerrariumTrigger);
        tab.show();
    }
};

// get pill id on load
getTabId();