<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
         pageEncoding="ISO-8859-1"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<%@ page isELIgnored="false" %>
<html>
<head>
<title>MEME CHAOS ZONE</title>
<style>
body{margin:0;min-height:100vh;font-family:"Comic Sans MS","Comic Sans",cursive;color:#fff;text-align:center;
  background:linear-gradient(270deg,#ff0080,#ff8c00,#ffee00,#00e676,#00b0ff,#d500f9,#ff0080);
  background-size:1400% 1400%;animation:bg 8s ease infinite;overflow-x:hidden}
@keyframes bg{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
@keyframes shake{0%{transform:translate(2px,1px) rotate(0)}25%{transform:translate(-3px,2px) rotate(-2deg)}
  50%{transform:translate(3px,-2px) rotate(2deg)}75%{transform:translate(-2px,-1px) rotate(-1deg)}100%{transform:translate(1px,2px) rotate(1deg)}}
@keyframes hue{from{filter:hue-rotate(0deg)}to{filter:hue-rotate(360deg)}}
@keyframes spin{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.15)}}
@keyframes rise{from{transform:translateY(0) rotate(0deg)}to{transform:translateY(-115vh) rotate(720deg)}}
@keyframes scroll{to{transform:translateX(-100%)}}
.marq{white-space:nowrap;overflow:hidden;background:#000;color:#ff0;font-size:1.4em;padding:6px}
.marq span{display:inline-block;padding-left:100%;animation:scroll 9s linear infinite}
h1{font-size:3.5em;margin:10px;text-shadow:3px 3px #000,-3px -3px #f0f;animation:shake .4s infinite,hue 3s linear infinite}
h2{background:#000;display:inline-block;padding:8px 16px;border:4px dashed #ff0;transform:rotate(-2deg);animation:pulse 1.5s infinite}
#logo{width:200px;border:6px ridge #0ff;border-radius:50%;animation:spin 6s linear infinite}
#meme{max-width:90%;border:8px double #fff;box-shadow:0 0 30px #f0f;transform:rotate(1deg)}
.btn{font-family:inherit;font-size:1.6em;font-weight:bold;padding:14px 28px;margin:12px;border:5px solid #fff;
  border-radius:20px;color:#fff;cursor:pointer;text-shadow:2px 2px #000;
  background:linear-gradient(45deg,#f0f,#0ff,#ff0);background-size:300% 300%;animation:bg 2s ease infinite,pulse 1s infinite}
#flag{display:none;font-size:2em;background:#000;color:#0f0;font-family:"Courier New",monospace;
  padding:12px;border:3px solid #0f0;margin:10px auto;max-width:90%;word-break:break-all}
.float{position:fixed;bottom:-60px;font-size:2em;pointer-events:none;z-index:5;animation-name:rise;
  animation-timing-function:linear;animation-iteration-count:infinite}
</style>
</head>
<body>
<div class="marq"><span>&#9889; WELCOME TO THE MEME CHAOS ZONE &#9889; REFRESH FOR MORE CHAOS &#9889; DO NOT PRESS THE BUTTON &#9889;</span></div>
<h2>Hello, my name is ${person.name}, I am ${person.age} years old.</h2>
<h1>Vit(ek) was here</h1>
<img id="logo" src="https://raw.githubusercontent.com/vpalaga/school_stuff/main/hack/logo.jpg" alt="Logo">
<br>
<img id="meme" src="" alt="Loading chaos...">
<br>
<button class="btn" onclick="loadMeme()">MORE CHAOS</button>
<button class="btn" onclick="revealFlag()">REVEAL THE FLAG</button>
<div id="flag"></div>
<script>
var memes = [
  ["drake", "Reading_the_error_message", "Rewriting_everything_from_scratch"],
  ["drake", "Sleeping_at_night", "One_more_bug_fix_at_3am"],
  ["buzz", "Console.log", "Console.log_everywhere"],
  ["rollsafe", "Cannot_have_bugs", "If_you_never_run_the_code"],
  ["spiderman", "The_code_I_wrote_at_2am", "The_code_I_read_at_9am"],
  ["cmm", "Friday_deployments_are_a_great_idea"],
  ["mordor", "One_does_not_simply", "Push_to_production_on_Friday"],
  ["fine", "The_server_is_on_fire", "This_is_fine"],
  ["success", "Fixed_one_bug", "Created_three_more"]
];
var base = "https://api.memegen.link/images/";
var tries = 0;
function loadMeme() {
  var m = memes[Math.floor(Math.random() * memes.length)];
  document.getElementById("meme").src = base + m.join("/") + ".png?width=500&r=" + Math.random();
}
document.getElementById("meme").onerror = function () { if (tries++ < 5) { loadMeme(); } };
function revealFlag() {
  var f = document.getElementById("flag");
  f.style.display = "block";
  f.innerHTML = "FLAG{n3v3r_g0nna_g1v3_y0u_up}";
  setTimeout(function () {
    window.location.href = "https://www.youtube.com/watch?v=dQw4w9WgXcQ";
  }, 1500);
}
var icons = ["\uD83C\uDF08", "\uD83D\uDE02", "\uD83D\uDD25", "\uD83D\uDC80", "\u2728", "\uD83E\uDD2A"];
for (var i = 0; i < 25; i++) {
  var s = document.createElement("div");
  s.className = "float";
  s.innerHTML = icons[Math.floor(Math.random() * icons.length)];
  s.style.left = Math.random() * 95 + "vw";
  s.style.animationDuration = (4 + Math.random() * 8) + "s";
  s.style.animationDelay = (Math.random() * 6) + "s";
  document.body.appendChild(s);
}
loadMeme();
</script>
</body>
</html>