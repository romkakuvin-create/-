const prizes = [
    { name: 'NFT', img: 'https://cdn-icons-png.flaticon.com/512/6298/6298154.png' },
    { name: 'Premium', img: 'https://cdn-icons-png.flaticon.com/512/5968/5968914.png' },
    { name: 'Stars', img: 'https://cdn-icons-png.flaticon.com/512/1828/1828884.png' },
    // Добавь остальные...
];

// В цикле отрисовки колеса:
let img = new Image();
img.src = prizes[i].imgUrl;
ctx.drawImage(img, x, y, width, height);
