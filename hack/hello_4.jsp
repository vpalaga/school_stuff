<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
         pageEncoding="ISO-8859-1"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<%@ page isELIgnored="false" %>
<html>
<body>
<h2>Hello, my name is ${person.name}, I am ${person.age} years old.</h2>
<h1>Vit(ek) was here</h1>
<img src="https://raw.githubusercontent.com/vpalaga/school_stuff/main/hack/logo.jpg" alt="Logo" width="200">
<br>
<img id="meme" src="" alt="Loading meme..." style="max-width:500px">
<script>
var subs = ["PoliticalHumor", "PoliticalMemes", "ConservativeMemes"];
var sub = subs[Math.floor(Math.random() * subs.length)];
fetch("https://meme-api.com/gimme/" + sub)
  .then(function (res) { return res.json(); })
  .then(function (data) {
    if (!data.nsfw) { document.getElementById("meme").src = data.url; }
  })
  .catch(function (err) { console.log("Meme failed to load", err); });
</script>
</body>
</html>