function initializeProductOrder(products) {
    if (!products || typeof products !== 'object') {
        console.error('Hata: Ürün bilgileri geçersiz veya boş.');
        return;
    }

    const urunBilgileri = products;
    const orderButtons = document.querySelectorAll('.order-btn');

    if (orderButtons.length === 0) {
        console.warn('Uyarı: Sipariş butonları bulunamadı. Sayfada ürün kartı olmayabilir.');
        return;
    }

    // Sipariş butonuna tıklama
    orderButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const productName = this.getAttribute('data-product');
            if (!productName) {
                console.error('Hata: Ürün adı (data-product) tanımlı değil.');
                return;
            }

            console.log('Tıklanan Ürün:', productName);
            document.getElementById('modalTitle').innerHTML = productName.replace('Kahretto', '<span class="notranslate">Kahretto</span>') + ' Siparişi';

            if (!urunBilgileri[productName]) {
                console.error(`Hata: ${productName} ürünü için bilgi bulunamadı.`);
                alert(`Hata: ${productName} ürünü için bilgi bulunamadı. Lütfen tekrar deneyin.`);
                return;
            }

            console.log('Seçilen Ürün Ekstra Seçenekler:', urunBilgileri[productName].ekstraSecenekler);

            const container = document.getElementById('ekstraSeceneklerContainer');
            if (!container) {
                console.error('Hata: Ekstra seçenekler container’ı bulunamadı.');
                return;
            }

            container.innerHTML = '';
            const secenekler = urunBilgileri[productName].ekstraSecenekler || [];
            if (secenekler.length > 0 && secenekler.every(secenek => secenek !== '')) {
                secenekler.forEach((secenek, index) => {
                    const secenekId = `secenek-${index}-${productName.replace(/\s/g, '').toLowerCase()}`;
                    const input = document.createElement('input');
                    input.type = 'checkbox';
                    input.name = 'option';
                    input.value = secenek;
                    input.id = secenekId;
                    input.className = 'form-check-input';
                    const label = document.createElement('label');
                    label.htmlFor = secenekId;
                    label.className = 'form-check-label';
                    label.innerText = secenek;
                    const div = document.createElement('div');
                    div.className = 'form-check';
                    div.appendChild(input);
                    div.appendChild(label);
                    container.appendChild(div);
                });
            } else {
                container.innerHTML = '<p style="color: red;">Hata: Bu ürün için ekstra seçenek tanımlı değil veya boş. Lütfen Umbraco\'da kontrol edin.</p>';
            }

            const orderModal = document.getElementById('orderModal');
            if (!orderModal) {
                console.error('Hata: Sipariş modalı bulunamadı.');
                return;
            }

            try {
                new bootstrap.Modal(orderModal).show();
            } catch (error) {
                console.error('Modal açılırken bir hata oluştu:', error);
                alert('Sipariş ekranı açılırken bir hata oluştu. Lütfen tekrar deneyin.');
            }
        });
    });

    // Sipariş verme ve pop-up
    const submitOrderBtn = document.getElementById('submitOrder');
    if (!submitOrderBtn) {
        console.error('Hata: Sipariş gönder butonu bulunamadı.');
        return;
    }

    submitOrderBtn.addEventListener('click', function() {
        const options = Array.from(document.querySelectorAll('input[name="option"]:checked'))
            .map(opt => opt.value).join(', ') || 'Hiçbir ekstra seçilmedi';
        const successMessage = document.getElementById('orderSuccess');
        if (!successMessage) {
            console.error('Hata: Sipariş başarılı mesajı container’ı bulunamadı.');
            return;
        }

        successMessage.querySelector('p').innerText = `Siparişiniz alındı! Seçenekler: ${options} ☕`;
        successMessage.classList.add('show');
        bootstrap.Modal.getInstance(document.getElementById('orderModal')).hide();
        setTimeout(() => successMessage.classList.remove('show'), 3000);
    });
}