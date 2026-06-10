class TarotCard {
    constructor(element) {
        this.element = element;
        this.isRevealed = false;
        this.init();
    }
    
    init() {
        this.element.addEventListener('click', () => this.toggle());
    }
    
    toggle() {
        this.isRevealed = !this.isRevealed;
        this.element.classList.toggle('revealed', this.isRevealed);
        
        if (this.isRevealed) {
            this.createSparkles();
        }
    }
    
    reveal() {
        this.isRevealed = true;
        this.element.classList.add('revealed');
        this.createSparkles();
    }
    
    hide() {
        this.isRevealed = false;
        this.element.classList.remove('revealed');
    }
    
    createSparkles() {
        const rect = this.element.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        
        for (let i = 0; i < 8; i++) {
            const sparkle = document.createElement('div');
            sparkle.className = 'card-sparkle';
            sparkle.style.left = centerX + 'px';
            sparkle.style.top = centerY + 'px';
            sparkle.style.setProperty('--sparkle-x', (Math.random() - 0.5) * 80 + 'px');
            sparkle.style.setProperty('--sparkle-y', (Math.random() - 0.5) * 80 + 'px');
            
            document.body.appendChild(sparkle);
            
            setTimeout(() => {
                sparkle.remove();
            }, 1000);
        }
    }
}

class CardSpread {
    constructor(container) {
        this.container = container;
        this.cards = [];
        this.revealedCount = 0;
        this.init();
    }
    
    init() {
        const cardSlots = this.container.querySelectorAll('.card-slot');
        cardSlots.forEach((slot, index) => {
            const card = new TarotCard(slot);
            this.cards.push(card);
            
            slot.style.animationDelay = (index * 0.1) + 's';
            slot.classList.add('card-appear');
        });
    }
    
    revealAll() {
        this.cards.forEach((card, index) => {
            setTimeout(() => {
                card.reveal();
                this.revealedCount++;
            }, index * 300);
        });
    }
    
    hideAll() {
        this.cards.forEach(card => {
            card.hide();
        });
        this.revealedCount = 0;
    }
    
    revealCard(index) {
        if (index >= 0 && index < this.cards.length) {
            this.cards[index].reveal();
            this.revealedCount++;
        }
    }
    
    getRevealedCount() {
        return this.revealedCount;
    }
    
    allRevealed() {
        return this.revealedCount === this.cards.length;
    }
}

class CardAnimator {
    static shuffle(cards, callback) {
        let shuffleCount = 0;
        const maxShuffles = 10;
        
        const shuffleInterval = setInterval(() => {
            cards.forEach(card => {
                const randomX = (Math.random() - 0.5) * 20;
                const randomY = (Math.random() - 0.5) * 20;
                const randomRotate = (Math.random() - 0.5) * 10;
                
                card.style.transform = `translate(${randomX}px, ${randomY}px) rotate(${randomRotate}deg)`;
            });
            
            shuffleCount++;
            
            if (shuffleCount >= maxShuffles) {
                clearInterval(shuffleInterval);
                
                cards.forEach(card => {
                    card.style.transform = '';
                });
                
                if (callback) {
                    callback();
                }
            }
        }, 100);
    }
    
    static flip(cardElement, callback) {
        cardElement.classList.add('flipping');
        
        setTimeout(() => {
            cardElement.classList.remove('flipping');
            cardElement.classList.add('flipped');
            
            if (callback) {
                callback();
            }
        }, 800);
    }
    
    static deal(cards, startX, startY, endPositions, callback) {
        cards.forEach((card, index) => {
            const endPos = endPositions[index];
            
            card.style.position = 'absolute';
            card.style.left = startX + 'px';
            card.style.top = startY + 'px';
            card.style.transition = 'all 0.5s ease';
            
            setTimeout(() => {
                card.style.left = endPos.x + 'px';
                card.style.top = endPos.y + 'px';
                card.style.transform = `rotate(${endPos.rotate || 0}deg)`;
            }, index * 200);
        });
        
        setTimeout(() => {
            if (callback) {
                callback();
            }
        }, cards.length * 200 + 500);
    }
    
    static revealWithGlow(cardElement) {
        cardElement.classList.add('glow-pulse');
        
        setTimeout(() => {
            cardElement.classList.remove('glow-pulse');
        }, 2000);
    }
    
    static revealSequentially(cards, callback) {
        cards.forEach((card, index) => {
            setTimeout(() => {
                card.classList.add('revealed');
                CardAnimator.revealWithGlow(card);
                
                if (index === cards.length - 1 && callback) {
                    setTimeout(callback, 500);
                }
            }, index * 500);
        });
    }
}

class CardEffects {
    static createMysticalAura(element) {
        const aura = document.createElement('div');
        aura.className = 'mystical-aura';
        element.appendChild(aura);
        
        return aura;
    }
    
    static addFloatingParticles(element, count = 5) {
        for (let i = 0; i < count; i++) {
            const particle = document.createElement('div');
            particle.className = 'floating-particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 3 + 's';
            particle.style.animationDuration = (Math.random() * 3 + 2) + 's';
            element.appendChild(particle);
        }
    }
    
    static createEnergyLine(startElement, endElement) {
        const startRect = startElement.getBoundingClientRect();
        const endRect = endElement.getBoundingClientRect();
        
        const startX = startRect.left + startRect.width / 2;
        const startY = startRect.top + startRect.height / 2;
        const endX = endRect.left + endRect.width / 2;
        const endY = endRect.top + endRect.height / 2;
        
        const length = Math.sqrt(Math.pow(endX - startX, 2) + Math.pow(endY - startY, 2));
        const angle = Math.atan2(endY - startY, endX - startX) * 180 / Math.PI;
        
        const line = document.createElement('div');
        line.className = 'energy-line';
        line.style.width = length + 'px';
        line.style.left = startX + 'px';
        line.style.top = startY + 'px';
        line.style.transform = `rotate(${angle}deg)`;
        
        document.body.appendChild(line);
        
        setTimeout(() => {
            line.remove();
        }, 2000);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const spreadContainers = document.querySelectorAll('.spread-layout');
    spreadContainers.forEach(container => {
        new CardSpread(container);
    });
    
    const singleCards = document.querySelectorAll('.card-display');
    singleCards.forEach(card => {
        new TarotCard(card);
    });
});
