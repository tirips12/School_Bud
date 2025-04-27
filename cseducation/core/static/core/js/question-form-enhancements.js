document.addEventListener('DOMContentLoaded', function() {
    console.log('Question form enhancements loading...');
    
    // Get the content textarea
    const contentTextarea = document.getElementById('id_content');
    
    if (!contentTextarea) {
        console.log('Content textarea not found');
        return;
    }
    
    console.log('Found content textarea, adding toolbar...');
    
    // Create toolbar container
    const toolbar = document.createElement('div');
    toolbar.className = 'bg-light border rounded p-2 mb-2 d-flex align-items-center';
    
    // Create code block button
    const codeBtn = document.createElement('button');
    codeBtn.type = 'button';
    codeBtn.className = 'btn btn-sm btn-outline-secondary me-2';
    codeBtn.innerHTML = '<i class="fas fa-code"></i> Code Block';
    
    // Add click handler for code button
    codeBtn.addEventListener('click', function(e) {
        e.preventDefault();
        
        const start = contentTextarea.selectionStart;
        const end = contentTextarea.selectionEnd;
        const selection = contentTextarea.value.substring(start, end);
        
        // Create code block with or without selected text
        let codeBlock;
        if (selection) {
            codeBlock = '```\n' + selection + '\n```';
        } else {
            codeBlock = '```\n// Your code here\n```';
        }
        
        // Insert at cursor position
        contentTextarea.value = 
            contentTextarea.value.substring(0, start) + 
            codeBlock + 
            contentTextarea.value.substring(end);
            
        // Set cursor position
        contentTextarea.focus();
        contentTextarea.setSelectionRange(start + codeBlock.length, start + codeBlock.length);
    });
    
    // Add help text
    const helpText = document.createElement('small');
    helpText.className = 'text-muted ms-2';
    helpText.textContent = 'Select text and click to format as code';
    
    // Add elements to toolbar
    toolbar.appendChild(codeBtn);
    toolbar.appendChild(helpText);
    
    // Insert toolbar before textarea
    contentTextarea.parentNode.insertBefore(toolbar, contentTextarea);
    
    console.log('Toolbar added successfully');
});
