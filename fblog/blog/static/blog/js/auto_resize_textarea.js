document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.auto-resize-textarea').forEach(textarea => {
        function autoResize() {
              textarea.style.height = '0px';

              const maxHeight = 200;

              const newHeight = Math.min(textarea.scrollHeight, maxHeight);
              console.log(textarea.scrollHeight)

              textarea.style.height = newHeight + 'px';

              if (textarea.scrollHeight > maxHeight) {
                textarea.style.overflowY = 'auto';
              } else {
                textarea.style.overflowY = 'hidden';
              }
            }

        textarea.addEventListener('input', autoResize);

        if (textarea.value.trim() !== '') {
            autoResize();
        }
    });
});