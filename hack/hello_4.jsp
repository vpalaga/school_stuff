<script>
var sub = "LinuxCirclejerk";
var tries = 0;
var fallbacks = [
  ["drake", "Reading_the_error_message", "Rewriting_everything_from_scratch"],
  ["buzz", "Console.log", "Console.log_everywhere"],
  ["spiderman", "The_code_I_wrote_at_2am", "The_code_I_read_at_9am"],
  ["fine", "The_server_is_on_fire", "This_is_fine"]
];
function fallbackMeme() {
  var m = fallbacks[Math.floor(Math.random() * fallbacks.length)];
  document.getElementById("meme").src =
    "https://api.memegen.link/images/" + m.join("/") + ".png?width=500&r=" + Math.random();
}
function loadMeme() {
  fetch("https://meme-api.com/gimme/" + sub)
    .then(function (res) { return res.json(); })
    .then(function (data) {
      if (data.url && !data.nsfw) {
        document.getElementById("meme").src = data.url;
      } else if (tries++ < 5) {
        loadMeme();
      } else {
        fallbackMeme();
      }
    })
    .catch(function () { fallbackMeme(); });
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