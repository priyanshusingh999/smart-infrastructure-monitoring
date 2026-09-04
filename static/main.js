// import '/js/app.js';
// import 'js/assistant.js';
// import 'js/dashboard.js';
// import 'js/progress.js';
// import 'js/risks.js';
// import 'js/schedule.js';


const scripts = [
    'static/js/app.js',
    'static/js/dashboard.js',
    'static/js/navigation.js',
    'static/js/progress.js',
    'static/js/assistant.js',
    'static/js/risks.js',
    'static/js/schedule.js',
    'static/js/upload.js',
    'static/js/signup.js'
];

for (const script of scripts) {
    const scriptElement = document.createElement('script');
    scriptElement.src = script;
    document.body.appendChild(scriptElement);
}