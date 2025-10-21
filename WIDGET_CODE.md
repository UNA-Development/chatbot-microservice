For LDP website:

```html
<!-- Add before closing </body> tag -->
<div id="rx4m-chatbot-container"></div>
<link rel="stylesheet" href="https://agenteva-microservices-b0a29780a00a.herokuapp.com/widget/chatbot.css">
<script src="https://agenteva-microservices-b0a29780a00a.herokuapp.com/widget/chatbot.js"></script>
<script>
  ChatbotWidget.init({
    apiUrl: 'https://agenteva-microservices-b0a29780a00a.herokuapp.com/',
    site: 'louisianadental'
  });
</script>
```

For Rx4Miracles website:

```html
<!-- Add before closing </body> tag -->
<div id="rx4m-chatbot-container"></div>
<link rel="stylesheet" href="https://agenteva-microservices-b0a29780a00a.herokuapp.com/widget/chatbot.css">
<script src="https://agenteva-microservices-b0a29780a00a.herokuapp.com/widget/chatbot.js"></script>
<script>
  ChatbotWidget.init({
    apiUrl: 'https://agenteva-microservices-b0a29780a00a.herokuapp.com/',
    site: 'rx4miracles'
  });
</script>
```