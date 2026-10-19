// data.json
// {"locked": [{
//     "s": "O1JiO9DvceqZNC0Xp9/P4Q==",
//     "i": "8e3YtRlbDE2vYJVE",
//     "c": "s4js7IIpQpC8oXLr6qvzrJNWE5UxCCUobwIw31xdx00rwznyeUyNC9D362iaOUkzQuTFG7wftGBfhqtgmMMf0q8Zl2kVVvRAOdFh0agYpzXkgNYi8r9JAteuX1yddvykCTQerqetk3qN8VgIXcmEuyuydpMFHxkRrqBYbS0rFDq3JxqGI82ZZq6bxb6dTzfb4BVXDoSQeOS91jyHnPOyaw/5AnXxoeei1Ye1axEM3mWNNzjcRM4YqVM2dhX4l5g9ARPxwmRWqWItFcSK37xhMYnbrXAz0t/BTjf5gNM4uT7+AQBs4hbVxmBg4EhdE/zMFKXPDdXCXal08K5k/XrL4nVVq8ZulAE4CllzqHOFfk8lrtwxImxREozzJ2iBsDqfWqxyZRAUaSa1m8CWF+8SJWTHvvb4HoesOpBx2iO0RQZfaBGSs23EOQ+lgxnp+CXSJAYpqEQIKsFrw+eK9hOQt2LKm4B7ONnYP/kpIZWN31aihl9lMeFynzkqxFbuo+QvWYPafT5VUJ/IbAem4V7Sej6pJeKdf4RhDmZcDkz3QGxGdReWk3gRWS0MCEOQBc9bLrY/NciS3ZppZ6uvzc/AzMIyDhsdKPjAFrn/MJJuFljzhUcC2A96JXMqSV3crJ9epeyei4MpQQHczYOw7AaG2EPqrweup5lTnKN3j2G8KfN2nm5yajpNjITKkQEmmieXtkI2SLWN7EdfbxBedsFxYwa/ZWXWcnEuHqhG+WslTsaAucSjrMtbawRVhOiAjUdN3b4DyJyg+hvjlVq+enRGp6MiVmM7thI/UDgsxQF0FySxDLM7gvTRnV1IsE90XNhtZrAatTccDg9gU0vTNemS6NCTJ4HgwwK6qDAgChwrRhUx9H8fRh0RokxR/TPFMKhsuO7c4VeLsb2qMv4rY+FYXYwBXrk/uDYdGxusU20xd6jFAMX6Af8t7KPqR9knbDc="
// }, {

async function unlock(n, answer) {
    const blob = DATA.locked[n];
    const base = await crypto.subtle.importKey('raw', enc.encode(norm(answer)), 'PBKDF2', false, ['deriveKey']);
    const key = await crypto.subtle.deriveKey({
        name: 'PBKDF2',
        salt: fromB64(blob.s),
        iterations: DATA.iter,
        hash: 'SHA-256'
    }, base, {
        name: 'AES-GCM',
        length: 256
    }, false, ['decrypt']);
    const plain = await crypto.subtle.decrypt({
        name: 'AES-GCM',
        iv: fromB64(blob.i)
    }, key, fromB64(blob.c));
    return JSON.parse(dec.decode(plain));
}