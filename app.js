// OrthoFinder - Main Application
// Alpine.js SPA with client-side routing

// Main App Controller
function app() {
    return {
        currentPage: 'home',
        mobileMenu: false,

        init() {
            // Handle browser back/forward
            window.addEventListener('popstate', (e) => {
                if (e.state && e.state.page) {
                    this.currentPage = e.state.page;
                }
            });

            // Listen for navigation events
            window.addEventListener('navigate', (e) => {
                this.navigate(e.detail);
            });

            // Check URL hash on load
            const hash = window.location.hash.slice(1);
            if (hash) {
                this.currentPage = hash;
            }
        },

        navigate(page) {
            this.currentPage = page;
            window.history.pushState({ page }, '', '#' + page);
            window.scrollTo({ top: 0, behavior: 'smooth' });
            this.mobileMenu = false;
        }
    };
}

// Home Page Component
function homePage() {
    return {
        openStep: 0,
        condition: '',
        state: '',
        city: '',
        conditionsList: [
            'Knee Pain / OA',
            'Lower Back / Disc Pain',
            'Shoulder / Rotator Cuff',
            'Hip Osteoarthritis',
            'Tennis Elbow / Epicondylitis',
            'Ankle / Achilles Tendon'
        ],
        statesList: ['California', 'Texas', 'Florida', 'New York', 'Arizona', 'Colorado', 'Mexico (Tourism)'],
        citiesData: {
            'California': ['Los Angeles', 'San Francisco', 'San Diego', 'Irvine'],
            'Texas': ['Houston', 'Austin', 'Dallas', 'San Antonio'],
            'Florida': ['Miami', 'Tampa', 'Orlando', 'Naples'],
            'Mexico (Tourism)': ['Tijuana', 'Cancun', 'Puerto Vallarta', 'Los Cabos']
        },
        pricingData: [
            { condition: 'Knee Therapy', range: '$3,500 - $6,200', count: 142 },
            { condition: 'Spine / Disc', range: '$5,000 - $9,500', count: 88 },
            { condition: 'Shoulder', range: '$3,000 - $5,500', count: 112 },
            { condition: 'Hip Joints', range: '$4,200 - $7,800', count: 94 }
        ],
        popularCities: [
            { name: 'Los Angeles', price: 'Avg $5,800', type: 'Premium', img: 'https://images.unsplash.com/photo-1580655653885-65763b2597ad?auto=format&fit=crop&w=300&q=80' },
            { name: 'Houston', price: 'Avg $4,900', type: 'Value', img: 'https://images.unsplash.com/photo-1530089711124-9ca31fb9e863?auto=format&fit=crop&w=300&q=80' },
            { name: 'Tijuana', price: 'Avg $2,800', type: 'Medical Tourism', img: 'https://images.unsplash.com/photo-1599351052796-039c381f9640?auto=format&fit=crop&w=300&q=80' },
            { name: 'Miami', price: 'Avg $6,100', type: 'Lifestyle', img: 'https://images.unsplash.com/photo-1514214246283-d427a95c5d2f?auto=format&fit=crop&w=300&q=80' },
            { name: 'Austin', price: 'Avg $5,200', type: 'Growth Hub', img: 'https://images.unsplash.com/photo-1531218150217-54595bc2b934?auto=format&fit=crop&w=300&q=80' }
        ],

        getCities() {
            return this.citiesData[this.state] || [];
        },

        performSearch() {
            if (this.condition && this.state && this.city) {
                if (this.city === 'Los Angeles') {
                    this.$dispatch('navigate', 'la-knee-results');
                } else if (this.state === 'Mexico (Tourism)') {
                    this.$dispatch('navigate', 'mexico-comparison');
                } else {
                    this.$dispatch('navigate', 'california-directory');
                }
            }
        },

        navigateToCity(cityName) {
            if (cityName === 'Los Angeles') {
                this.$dispatch('navigate', 'la-directory');
            } else if (cityName === 'Tijuana') {
                this.$dispatch('navigate', 'mexico-comparison');
            } else {
                this.$dispatch('navigate', 'california-directory');
            }
        }
    };
}

// Cost Index Page Component
function costIndexPage() {
    return {
        search: '',
        sortBy: 'name',
        pricingData: [
            { id: 1, name: 'Knee Osteoarthritis', low: 3000, median: 5500, high: 8000, clinics: 142, trend: 'up', trendPercent: 4.2 },
            { id: 2, name: 'Lumbar Spine / Disc', low: 5000, median: 8200, high: 12500, clinics: 88, trend: 'down', trendPercent: 1.5 },
            { id: 3, name: 'Shoulder (Rotator Cuff)', low: 3500, median: 5800, high: 7500, clinics: 112, trend: 'up', trendPercent: 2.8 },
            { id: 4, name: 'Hip Osteoarthritis', low: 4000, median: 6500, high: 9000, clinics: 94, trend: 'up', trendPercent: 3.1 },
            { id: 5, name: 'Cervical Spine (Neck)', low: 4500, median: 7800, high: 11000, clinics: 56, trend: 'up', trendPercent: 5.4 },
            { id: 6, name: 'Ankle / Achilles', low: 2500, median: 4200, high: 6000, clinics: 74, trend: 'down', trendPercent: 0.8 },
            { id: 7, name: "Tennis/Golfer's Elbow", low: 2000, median: 3500, high: 5200, clinics: 105, trend: 'down', trendPercent: 2.2 },
            { id: 8, name: 'Sacroiliac (SI) Joint', low: 4000, median: 6200, high: 8500, clinics: 42, trend: 'up', trendPercent: 1.9 },
            { id: 9, name: 'Wrist / Hand Arthritis', low: 2800, median: 4500, high: 6800, clinics: 63, trend: 'up', trendPercent: 2.5 },
            { id: 10, name: 'Plantar Fasciitis', low: 1800, median: 3200, high: 4800, clinics: 120, trend: 'down', trendPercent: 4.1 }
        ],
        priceDrivers: [
            { title: 'Cell Source', desc: 'BMAC is typically 20-40% more expensive than Adipose derived options.', impact: '+ $1,500 - $3,000' },
            { title: 'Image Guidance', desc: 'Fluoroscopy or Ultrasound for precision placement increases costs.', impact: '+ $500 - $1,200' },
            { title: 'Facility Level', desc: 'Hospital outpatient costs more than private office suite.', impact: '+ $2,000 - $5,000' }
        ],

        init() {
            this.$nextTick(() => this.renderCostIndexContent());
        },

        get filteredPricing() {
            let filtered = this.pricingData.filter(i => i.name.toLowerCase().includes(this.search.toLowerCase()));
            if (this.sortBy === 'name') return filtered.sort((a, b) => a.name.localeCompare(b.name));
            if (this.sortBy === 'median') return filtered.sort((a, b) => b.median - a.median);
            if (this.sortBy === 'clinics') return filtered.sort((a, b) => b.clinics - a.clinics);
            return filtered;
        },

        renderCostIndexContent() {
            this.$el.innerHTML = `
                <div class="py-8 md:py-12">
                    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <nav class="flex mb-8 text-xs font-bold uppercase tracking-widest text-slate-400 gap-2">
                            <a href="#" @click.prevent="$dispatch('navigate', 'home')" class="hover:text-brand-600">Home</a>
                            <span>/</span>
                            <span class="text-slate-600">National Cost Index</span>
                        </nav>
                        <div class="mb-12">
                            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 text-white text-[10px] font-bold uppercase tracking-widest mb-4">
                                <span class="w-2 h-2 rounded-full bg-green-400 animate-pulse"></span>
                                Verified Data Report: Q1 2026
                            </div>
                            <h1 class="text-3xl md:text-5xl font-extrabold text-slate-900 tracking-tight mb-4">
                                National Stem Cell <span class="text-brand-600">Cost Index</span>
                            </h1>
                            <p class="text-lg text-slate-600 max-w-3xl">
                                Comprehensive median pricing across 10 orthopedic categories. These ranges represent typical out-of-pocket costs for cash-pay patients in the United States.
                            </p>
                        </div>

                        <div class="bg-white rounded-3xl shadow-xl shadow-brand-100/50 border border-slate-100 overflow-hidden">
                            <div class="p-6 border-b border-slate-100 flex flex-col md:flex-row justify-between items-center gap-4 bg-slate-50/50">
                                <div class="relative w-full md:w-72">
                                    <input type="text" x-model="search" placeholder="Search conditions..." class="w-full pl-10 pr-4 py-2.5 bg-white border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-brand-500 focus:border-brand-500 transition-all outline-none">
                                    <svg class="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                                </div>
                                <div class="flex items-center gap-2">
                                    <span class="text-xs font-bold text-slate-400 uppercase">Sort By:</span>
                                    <select x-model="sortBy" class="text-sm font-semibold text-slate-700 bg-transparent border-none focus:ring-0 cursor-pointer">
                                        <option value="name">Condition Name</option>
                                        <option value="median">Median Price</option>
                                        <option value="clinics">Clinic Volume</option>
                                    </select>
                                </div>
                            </div>

                            <div class="hidden md:grid grid-cols-12 px-8 py-4 bg-white border-b border-slate-100 text-[10px] font-bold uppercase tracking-widest text-slate-400">
                                <div class="col-span-4">Condition & Sample Size</div>
                                <div class="col-span-2 text-center">National Low</div>
                                <div class="col-span-3 text-center">Median Benchmark</div>
                                <div class="col-span-2 text-center">National High</div>
                                <div class="col-span-1 text-right">Trend</div>
                            </div>

                            <div class="divide-y divide-slate-50">
                                <template x-for="item in filteredPricing" :key="item.id">
                                    <div class="px-6 md:px-8 py-6 table-row-hover transition-colors group cursor-pointer" @click="$dispatch('navigate', 'knee-cost-guide')">
                                        <div class="grid grid-cols-1 md:grid-cols-12 items-center gap-4 md:gap-0">
                                            <div class="col-span-1 md:col-span-4 flex items-center gap-4">
                                                <div class="w-10 h-10 rounded-xl bg-brand-50 flex items-center justify-center text-brand-600 group-hover:bg-brand-600 group-hover:text-white transition-all">
                                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
                                                </div>
                                                <div>
                                                    <h3 class="font-bold text-slate-900 group-hover:text-brand-600 transition-colors" x-text="item.name"></h3>
                                                    <span class="text-[10px] text-slate-400 font-bold uppercase" x-text="item.clinics + ' Reports Indexed'"></span>
                                                </div>
                                            </div>
                                            <div class="col-span-1 md:col-span-2 text-center">
                                                <span class="text-sm font-bold text-slate-500" x-text="'$' + item.low.toLocaleString()"></span>
                                            </div>
                                            <div class="col-span-1 md:col-span-3 text-center">
                                                <div class="inline-flex flex-col items-center">
                                                    <span class="text-xl font-extrabold text-slate-900 leading-none mb-1" x-text="'$' + item.median.toLocaleString()"></span>
                                                    <div class="w-24 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                                                        <div class="h-full price-range-fill rounded-full" :style="'width: ' + ((item.median - item.low) / (item.high - item.low) * 100) + '%'"></div>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="col-span-1 md:col-span-2 text-center">
                                                <span class="text-sm font-bold text-slate-500" x-text="'$' + item.high.toLocaleString()"></span>
                                            </div>
                                            <div class="col-span-1 md:col-span-1 text-right">
                                                <div class="inline-flex items-center gap-1" :class="item.trend === 'up' ? 'text-rose-500' : 'text-emerald-500'">
                                                    <svg class="w-4 h-4" :class="item.trend === 'up' ? '' : 'rotate-180'" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path></svg>
                                                    <span class="text-[10px] font-extrabold" x-text="item.trendPercent + '%'"></span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </template>
                            </div>

                            <div class="p-6 bg-slate-50 border-t border-slate-100 flex flex-col md:flex-row justify-between items-center gap-4">
                                <p class="text-xs text-slate-500 font-medium">Showing 10 of 10 major orthopedic conditions</p>
                                <button class="flex items-center gap-2 text-brand-600 font-bold text-sm hover:underline">
                                    Request Full PDF Report (Free)
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }
    };
}

// Knee Cost Guide Page Component
function kneeCostGuidePage() {
    return {
        cityPrices: [
            { name: 'Los Angeles', state: 'California', price: '$5,800', supply: 5, trend: 'none' },
            { name: 'Houston', state: 'Texas', price: '$4,950', supply: 4, trend: 'down' },
            { name: 'Miami', state: 'Florida', price: '$6,200', supply: 5, trend: 'none' },
            { name: 'Austin', state: 'Texas', price: '$5,400', supply: 3, trend: 'none' },
            { name: 'Phoenix', state: 'Arizona', price: '$4,100', supply: 4, trend: 'down' },
            { name: 'Denver', state: 'Colorado', price: '$5,150', supply: 3, trend: 'none' },
            { name: 'Tijuana', state: 'Mexico (Tourism)', price: '$2,850', supply: 5, trend: 'down' }
        ],

        init() {
            this.$nextTick(() => this.renderContent());
        },

        renderContent() {
            this.$el.innerHTML = `
                <section class="pt-8 pb-12">
                    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
                        <nav class="flex mb-4 text-xs font-bold uppercase tracking-wider text-slate-400 gap-2 items-center">
                            <a href="#" @click.prevent="$dispatch('navigate', 'home')" class="hover:text-brand-600">Home</a>
                            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"></path></svg>
                            <a href="#" @click.prevent="$dispatch('navigate', 'cost-index')" class="hover:text-brand-600">Cost Guides</a>
                            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"></path></svg>
                            <span class="text-brand-600">Knee Therapy</span>
                        </nav>
                        <h1 class="text-3xl md:text-5xl font-extrabold text-slate-900 tracking-tight mb-4">
                            Knee Stem Cell Injection <br class="hidden md:block">
                            <span class="text-brand-600">Cost Guide & Price Estimates</span>
                        </h1>
                        <p class="text-lg text-slate-600 max-w-3xl leading-relaxed">
                            How much does stem cell therapy for knees actually cost? We analyzed data from 500+ clinics to provide realistic price ranges.
                        </p>
                    </div>
                </section>

                <section class="pb-16">
                    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div class="bg-white rounded-[2rem] shadow-xl shadow-brand-100/50 border border-slate-100 p-8 md:p-12 relative overflow-hidden">
                            <h2 class="text-xl font-bold text-slate-900 mb-10 flex items-center gap-2">
                                <span class="w-8 h-8 rounded-lg bg-brand-600 flex items-center justify-center text-white text-sm">$</span>
                                National Estimated Price Range
                            </h2>
                            <div class="relative pt-12 pb-8">
                                <div class="h-4 w-full bg-slate-100 rounded-full overflow-hidden flex">
                                    <div class="h-full price-gradient-bar w-full"></div>
                                </div>
                                <div class="absolute top-0 left-0 w-full h-full pointer-events-none">
                                    <div class="absolute left-[15%] -top-4 text-center">
                                        <div class="w-0.5 h-20 bg-slate-200 mx-auto mb-2"></div>
                                        <span class="block text-[10px] font-bold text-slate-400 uppercase">Min Reported</span>
                                        <span class="text-xl font-extrabold text-slate-700">$2,900</span>
                                    </div>
                                    <div class="absolute left-1/2 -translate-x-1/2 -top-12 text-center">
                                        <div class="bg-brand-600 text-white px-3 py-1 rounded-full text-xs font-bold mb-2 shadow-lg shadow-brand-200">National Median</div>
                                        <div class="w-1 h-28 bg-brand-600 mx-auto mb-2"></div>
                                        <span class="text-3xl font-black text-brand-600">$4,850</span>
                                        <span class="block text-[10px] font-bold text-slate-400 uppercase mt-1">Single Knee / BMAC</span>
                                    </div>
                                    <div class="absolute right-[10%] -top-4 text-center">
                                        <div class="w-0.5 h-20 bg-slate-200 mx-auto mb-2"></div>
                                        <span class="block text-[10px] font-bold text-slate-400 uppercase">Max (Premium)</span>
                                        <span class="text-xl font-extrabold text-slate-700">$8,200+</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                <section class="py-16 bg-slate-900 text-white">
                    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
                        <h2 class="text-3xl font-extrabold mb-8">What Drives Knee Treatment Costs?</h2>
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                            <div class="bg-slate-800 p-8 rounded-3xl border border-slate-700">
                                <div class="absolute -top-4 -right-4 w-12 h-12 bg-sky-500 rounded-2xl flex items-center justify-center font-bold shadow-lg">1</div>
                                <h3 class="text-lg font-bold mb-4">Cell Source</h3>
                                <p class="text-slate-400 text-sm">BMAC (Bone Marrow) is the orthopedic gold standard. Adipose-derived is typically cheaper.</p>
                            </div>
                            <div class="bg-slate-800 p-8 rounded-3xl border border-slate-700">
                                <h3 class="text-lg font-bold mb-4">Procedure Scope</h3>
                                <div class="space-y-2 text-sm">
                                    <div class="flex justify-between border-b border-slate-700 pb-2">
                                        <span class="text-slate-300">Unilateral (1 Knee)</span>
                                        <span class="font-bold">$3,500+</span>
                                    </div>
                                    <div class="flex justify-between border-b border-slate-700 pb-2">
                                        <span class="text-slate-300">Bilateral (2 Knees)</span>
                                        <span class="font-bold">$5,500+</span>
                                    </div>
                                </div>
                            </div>
                            <div class="bg-slate-800 p-8 rounded-3xl border border-slate-700">
                                <h3 class="text-lg font-bold mb-4">Location Type</h3>
                                <p class="text-slate-400 text-sm">Private clinics are typically median pricing. Hospital outpatient departments cost significantly more.</p>
                            </div>
                        </div>
                    </div>
                </section>

                <section class="py-20 bg-white">
                    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
                        <h2 class="text-2xl font-extrabold text-slate-900 mb-8">Price by Major Metro Area</h2>
                        <div class="border border-slate-200 rounded-2xl overflow-hidden shadow-sm">
                            <table class="w-full text-left border-collapse">
                                <thead>
                                    <tr class="bg-slate-50 border-b border-slate-200">
                                        <th class="px-6 py-4 text-[10px] font-bold uppercase tracking-widest text-slate-400">City / Region</th>
                                        <th class="px-6 py-4 text-[10px] font-bold uppercase tracking-widest text-slate-400">Avg. Quote</th>
                                        <th class="px-6 py-4 text-[10px] font-bold uppercase tracking-widest text-slate-400">Supply</th>
                                        <th class="px-6 py-4 text-[10px] font-bold uppercase tracking-widest text-slate-400 text-right">Action</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-slate-100">
                                    <template x-for="city in cityPrices" :key="city.name">
                                        <tr class="hover:bg-brand-50/30 transition-colors group cursor-pointer" @click="city.name === 'Los Angeles' ? $dispatch('navigate', 'la-knee-results') : (city.name === 'Tijuana' ? $dispatch('navigate', 'mexico-comparison') : null)">
                                            <td class="px-6 py-4">
                                                <span class="font-bold text-slate-700" x-text="city.name"></span>
                                                <span class="block text-[10px] text-slate-400 font-medium" x-text="city.state"></span>
                                            </td>
                                            <td class="px-6 py-4">
                                                <span class="font-bold text-brand-600" x-text="city.price"></span>
                                            </td>
                                            <td class="px-6 py-4">
                                                <div class="flex gap-1">
                                                    <template x-for="i in 5">
                                                        <div :class="i <= city.supply ? 'bg-brand-400' : 'bg-slate-200'" class="w-1.5 h-3 rounded-full"></div>
                                                    </template>
                                                </div>
                                            </td>
                                            <td class="px-6 py-4 text-right">
                                                <button class="text-xs font-bold text-slate-400 group-hover:text-brand-600 flex items-center gap-1 justify-end ml-auto transition">
                                                    View Clinics <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"></path></svg>
                                                </button>
                                            </td>
                                        </tr>
                                    </template>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </section>

                <section class="py-12">
                    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div class="bg-gradient-to-br from-brand-600 to-sky-600 rounded-[2.5rem] p-10 md:p-16 text-center text-white relative overflow-hidden shadow-2xl shadow-brand-200">
                            <h2 class="text-3xl font-extrabold mb-6">Find Verified Knee Clinics Near You</h2>
                            <p class="text-brand-100 text-lg mb-10 max-w-2xl mx-auto">Get connected with orthopedic specialists who publish their price ranges upfront.</p>
                            <button @click="$dispatch('navigate', 'la-knee-results')" class="px-10 py-4 bg-slate-900 text-white rounded-2xl font-extrabold hover:bg-slate-800 transition">
                                Search Knee Clinics
                            </button>
                        </div>
                    </div>
                </section>
            `;
        }
    };
}

// LA Knee Results Page
function laKneeResultsPage() {
    return {
        sortBy: 'featured',
        priceOnly: false,
        clinics: [
            { id: 1, name: 'Regenexx Los Angeles', address: '11500 Olympic Blvd, Los Angeles, CA', image: 'https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=300&q=80', distance: 2.4, rating: 5, reviews: 84, featured: true, priceRange: '$5,500 - $7,200', tags: ['Board Certified', 'Ultrasound Guided'], financing: true },
            { id: 2, name: 'LA Orthopedic & Regenerative', address: 'Beverly Hills, CA', image: 'https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&w=300&q=80', distance: 4.8, rating: 4, reviews: 52, featured: false, priceRange: '$4,800 - $6,500', tags: ['Fluoroscopy', 'Orthopedic Specialist'], financing: false },
            { id: 3, name: 'Santa Monica Stem Cell Institute', address: 'Santa Monica, CA', image: 'https://images.unsplash.com/photo-1631217868264-e5b90bb7e133?auto=format&fit=crop&w=300&q=80', distance: 6.2, rating: 4, reviews: 31, featured: false, priceRange: '$3,900 - $5,200', tags: ['Value Pricing'], financing: false }
        ],

        init() {
            this.$nextTick(() => this.renderContent());
        },

        filteredClinics() {
            let result = this.clinics;
            if (this.priceOnly) result = result.filter(c => c.priceRange !== null);
            if (this.sortBy === 'featured') result = result.sort((a, b) => b.featured - a.featured);
            return result;
        },

        renderContent() {
            this.$el.innerHTML = `
                <div class="bg-white border-b border-slate-200 py-4">
                    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <nav class="flex text-xs font-bold text-slate-400 uppercase tracking-widest gap-2 items-center">
                            <a href="#" @click.prevent="$dispatch('navigate', 'home')" class="hover:text-brand-600">USA</a>
                            <span>/</span>
                            <a href="#" @click.prevent="$dispatch('navigate', 'california-directory')" class="hover:text-brand-600">California</a>
                            <span>/</span>
                            <span class="text-slate-900">Los Angeles</span>
                        </nav>
                    </div>
                </div>

                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                    <div class="mb-6">
                        <h1 class="text-2xl font-extrabold text-slate-900">Knee Stem Cell Therapy in Los Angeles</h1>
                        <p class="text-slate-500 text-sm mt-1" x-text="filteredClinics().length + ' clinics found'"></p>
                    </div>

                    <div class="space-y-4">
                        <template x-for="clinic in filteredClinics()" :key="clinic.id">
                            <div :class="clinic.featured ? 'featured-card bg-white' : 'bg-white border border-slate-200'" class="rounded-3xl p-6 transition-all hover:shadow-lg relative">
                                <div x-show="clinic.featured" class="absolute top-0 right-0 bg-brand-600 text-white px-4 py-1 rounded-bl-2xl text-[10px] font-black uppercase">Featured</div>
                                <div class="flex flex-col md:flex-row gap-6">
                                    <div class="md:w-1/4">
                                        <div class="aspect-square rounded-2xl bg-slate-100 overflow-hidden">
                                            <img :src="clinic.image" class="w-full h-full object-cover">
                                        </div>
                                    </div>
                                    <div class="md:w-2/4">
                                        <h3 class="text-xl font-extrabold text-slate-900" x-text="clinic.name"></h3>
                                        <p class="text-sm text-slate-500 mb-3" x-text="clinic.address"></p>
                                        <div class="flex flex-wrap gap-2 mb-4">
                                            <template x-for="tag in clinic.tags">
                                                <span class="px-2 py-1 bg-slate-50 text-slate-500 rounded-md text-[10px] font-bold border border-slate-100" x-text="tag"></span>
                                            </template>
                                        </div>
                                        <template x-if="clinic.priceRange">
                                            <div class="price-badge-glow inline-flex flex-col px-4 py-2 bg-gradient-to-br from-brand-600 to-sky-500 rounded-xl text-white">
                                                <span class="text-[9px] uppercase font-black opacity-80">Published Price</span>
                                                <span class="text-lg font-black" x-text="clinic.priceRange"></span>
                                            </div>
                                        </template>
                                    </div>
                                    <div class="md:w-1/4 flex flex-col justify-center gap-3 border-t md:border-t-0 md:border-l border-slate-100 pt-4 md:pt-0 md:pl-6">
                                        <button class="w-full bg-brand-600 hover:bg-brand-700 text-white font-bold py-3 px-4 rounded-xl flex items-center justify-center gap-2">
                                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path></svg>
                                            Call Now
                                        </button>
                                        <button @click="$dispatch('navigate', 'clinic-profile')" class="w-full bg-white hover:bg-slate-50 text-slate-700 border-2 border-slate-100 font-bold py-3 px-4 rounded-xl">
                                            View Profile
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </template>
                    </div>
                </div>
            `;
        }
    };
}

// Clinic Profile Page
function clinicProfilePage() {
    return {
        activeTab: 'conditions',
        showNumber: false,
        procedures: [
            { name: 'Knee BMAC Injection', price: '$4,500 - $6,000', details: 'Includes MRI review and ultrasound guidance.' },
            { name: 'Spine / Lumbar Disc (PRP)', price: '$2,800 - $3,500', details: 'Fluoroscopy-guided intradiscal injection.' },
            { name: 'Shoulder Rotator Cuff', price: '$4,200 - $5,500', details: 'Targets partial tears and severe bursitis.' }
        ],

        init() {
            this.$nextTick(() => this.renderContent());
        },

        renderContent() {
            this.$el.innerHTML = `
                <section class="bg-white border-b border-slate-200 py-8 lg:py-12">
                    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <nav class="flex text-xs font-bold text-slate-400 uppercase tracking-widest mb-6 gap-2 items-center">
                            <a href="#" @click.prevent="$dispatch('navigate', 'california-directory')" class="hover:text-brand-600">California</a>
                            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"></path></svg>
                            <a href="#" @click.prevent="$dispatch('navigate', 'la-directory')" class="hover:text-brand-600">Los Angeles</a>
                        </nav>
                        <div class="flex items-center gap-3 mb-3">
                            <span class="px-2.5 py-1 bg-brand-600 text-white text-[10px] font-black uppercase rounded">Featured</span>
                            <span class="text-emerald-600 bg-emerald-50 px-2 py-1 rounded text-xs font-bold border border-emerald-100">Price Published</span>
                        </div>
                        <h1 class="text-3xl md:text-5xl font-extrabold text-slate-900 tracking-tight mb-2">
                            Pacific Coast Regenerative Orthopedics
                        </h1>
                        <p class="flex items-center gap-1.5 font-medium text-slate-500">
                            <svg class="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                            2200 Santa Monica Blvd, Ste 105, Santa Monica, CA 90404
                        </p>
                    </div>
                </section>

                <section class="py-12">
                    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div class="grid grid-cols-1 lg:grid-cols-12 gap-12">
                            <div class="lg:col-span-8">
                                <div class="flex border-b border-slate-200 mb-8">
                                    <button @click="activeTab = 'conditions'" :class="activeTab === 'conditions' ? 'tab-active border-b-2' : 'text-slate-500'" class="px-6 py-4 font-bold transition-all">Conditions & Pricing</button>
                                    <button @click="activeTab = 'credentials'" :class="activeTab === 'credentials' ? 'tab-active border-b-2' : 'text-slate-500'" class="px-6 py-4 font-bold transition-all">Physicians</button>
                                </div>

                                <div x-show="activeTab === 'conditions'">
                                    <div class="bg-white rounded-3xl border border-slate-200 overflow-hidden mb-12">
                                        <div class="p-6 border-b border-slate-100 bg-slate-50/50">
                                            <h3 class="font-extrabold text-lg">Reported Treatment Costs</h3>
                                        </div>
                                        <div class="divide-y divide-slate-100">
                                            <template x-for="item in procedures" :key="item.name">
                                                <div class="p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4 group hover:bg-slate-50 transition">
                                                    <div>
                                                        <h4 class="font-bold text-slate-900" x-text="item.name"></h4>
                                                        <p class="text-xs text-slate-500" x-text="item.details"></p>
                                                    </div>
                                                    <div class="flex flex-col sm:items-end">
                                                        <span class="text-xl font-extrabold text-brand-700" x-text="item.price"></span>
                                                        <span class="text-[10px] font-bold text-slate-400 uppercase">Estimated per session</span>
                                                    </div>
                                                </div>
                                            </template>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div class="lg:col-span-4">
                                <div class="sticky sticky-sidebar bg-white rounded-3xl p-6 border border-slate-200 shadow-xl">
                                    <h3 class="font-extrabold text-xl mb-6">Contact Clinic</h3>
                                    <button class="w-full bg-slate-900 text-white py-4 rounded-2xl font-bold hover:bg-black transition-all mb-3 flex items-center justify-center gap-2">
                                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path></svg>
                                        Call Now
                                    </button>
                                    <p class="text-center text-[11px] text-slate-400">Consultation Fee: $150 (Applied to treatment)</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            `;
        }
    };
}

// California Directory Page
function californiaDirectoryPage() {
    return {
        cities: [
            { name: 'Los Angeles', clinics: 42, avgPrice: '$5,800' },
            { name: 'San Francisco', clinics: 28, avgPrice: '$6,200' },
            { name: 'San Diego', clinics: 24, avgPrice: '$5,400' },
            { name: 'Irvine', clinics: 18, avgPrice: '$5,600' },
            { name: 'Sacramento', clinics: 12, avgPrice: '$4,800' }
        ],

        init() {
            this.$nextTick(() => this.renderContent());
        },

        renderContent() {
            this.$el.innerHTML = `
                <section class="py-8 md:py-12">
                    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <nav class="flex mb-8 text-xs font-bold uppercase tracking-widest text-slate-400 gap-2">
                            <a href="#" @click.prevent="$dispatch('navigate', 'home')" class="hover:text-brand-600">Home</a>
                            <span>/</span>
                            <span class="text-slate-600">California</span>
                        </nav>

                        <h1 class="text-3xl md:text-5xl font-extrabold text-slate-900 tracking-tight mb-4">
                            Stem Cell Clinics in <span class="text-brand-600">California</span>
                        </h1>
                        <p class="text-lg text-slate-600 max-w-3xl mb-12">
                            Browse 124 verified regenerative medicine clinics across the Golden State.
                        </p>

                        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            <template x-for="city in cities" :key="city.name">
                                <div @click="city.name === 'Los Angeles' ? $dispatch('navigate', 'la-directory') : null" class="bg-white rounded-3xl p-6 border border-slate-200 hover:shadow-xl hover:-translate-y-1 transition-all cursor-pointer group">
                                    <h3 class="text-xl font-extrabold text-slate-900 mb-2 group-hover:text-brand-600" x-text="city.name"></h3>
                                    <div class="flex items-center gap-4 text-sm text-slate-500 mb-4">
                                        <span x-text="city.clinics + ' Clinics'"></span>
                                        <span>|</span>
                                        <span x-text="'Avg ' + city.avgPrice"></span>
                                    </div>
                                    <div class="flex items-center justify-between">
                                        <span class="text-xs font-bold text-brand-600">View All</span>
                                        <svg class="w-4 h-4 text-brand-600 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                                    </div>
                                </div>
                            </template>
                        </div>
                    </div>
                </section>
            `;
        }
    };
}

// LA Directory Page
function laDirectoryPage() {
    return {
        clinics: [
            { name: 'Regenexx Los Angeles', specialty: 'BMAC & PRP', price: '$5,500 - $7,200', featured: true },
            { name: 'LA Orthopedic Center', specialty: 'All Conditions', price: '$4,800 - $6,500', featured: false },
            { name: 'Santa Monica Institute', specialty: 'Knee & Hip', price: '$3,900 - $5,200', featured: false }
        ],

        init() {
            this.$nextTick(() => this.renderContent());
        },

        renderContent() {
            this.$el.innerHTML = `
                <section class="py-8 md:py-12">
                    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <nav class="flex mb-8 text-xs font-bold uppercase tracking-widest text-slate-400 gap-2">
                            <a href="#" @click.prevent="$dispatch('navigate', 'home')" class="hover:text-brand-600">Home</a>
                            <span>/</span>
                            <a href="#" @click.prevent="$dispatch('navigate', 'california-directory')" class="hover:text-brand-600">California</a>
                            <span>/</span>
                            <span class="text-slate-600">Los Angeles</span>
                        </nav>

                        <h1 class="text-3xl md:text-5xl font-extrabold text-slate-900 tracking-tight mb-4">
                            Stem Cell Clinics in <span class="text-brand-600">Los Angeles</span>
                        </h1>
                        <p class="text-lg text-slate-600 max-w-3xl mb-12">
                            42 verified regenerative medicine clinics in the Los Angeles metro area.
                        </p>

                        <div class="space-y-4">
                            <template x-for="clinic in clinics" :key="clinic.name">
                                <div :class="clinic.featured ? 'featured-card' : 'border border-slate-200'" class="bg-white rounded-3xl p-6 hover:shadow-lg transition-all cursor-pointer" @click="$dispatch('navigate', 'clinic-profile')">
                                    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                                        <div>
                                            <div x-show="clinic.featured" class="inline-block px-2 py-1 bg-brand-600 text-white text-[10px] font-black uppercase rounded mb-2">Featured</div>
                                            <h3 class="text-xl font-extrabold text-slate-900" x-text="clinic.name"></h3>
                                            <p class="text-sm text-slate-500" x-text="clinic.specialty"></p>
                                        </div>
                                        <div class="flex items-center gap-4">
                                            <div class="text-right">
                                                <span class="text-xs text-slate-400 uppercase font-bold">Price Range</span>
                                                <p class="text-lg font-extrabold text-brand-600" x-text="clinic.price"></p>
                                            </div>
                                            <button class="bg-brand-600 text-white px-6 py-3 rounded-xl font-bold hover:bg-brand-700 transition">
                                                View Profile
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </template>
                        </div>
                    </div>
                </section>
            `;
        }
    };
}

// Mexico Comparison Page
function mexicoComparisonPage() {
    return {
        comparisons: [
            { treatment: 'Knee (Single)', us: '$5,500', mexico: '$2,800', savings: '49%' },
            { treatment: 'Knee (Both)', us: '$8,500', mexico: '$4,200', savings: '51%' },
            { treatment: 'Hip OA', us: '$6,500', mexico: '$3,200', savings: '51%' },
            { treatment: 'IV Stem Cell', us: '$12,000', mexico: '$4,500', savings: '63%' }
        ],

        init() {
            this.$nextTick(() => this.renderContent());
        },

        renderContent() {
            this.$el.innerHTML = `
                <section class="py-8 md:py-12">
                    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <nav class="flex mb-8 text-xs font-bold uppercase tracking-widest text-slate-400 gap-2">
                            <a href="#" @click.prevent="$dispatch('navigate', 'home')" class="hover:text-brand-600">Home</a>
                            <span>/</span>
                            <span class="text-slate-600">Mexico Medical Tourism</span>
                        </nav>

                        <div class="flex items-center gap-4 mb-6">
                            <span class="text-4xl">🇲🇽</span>
                            <div>
                                <h1 class="text-3xl md:text-5xl font-extrabold text-slate-900 tracking-tight">
                                    Mexico <span class="text-brand-600">Medical Tourism</span>
                                </h1>
                                <p class="text-lg text-slate-600">Compare US vs Mexico stem cell therapy costs</p>
                            </div>
                        </div>

                        <div class="bg-white rounded-3xl border border-slate-200 overflow-hidden mb-12">
                            <div class="p-6 bg-slate-50 border-b border-slate-200">
                                <h3 class="font-extrabold text-lg">Price Comparison: US vs Mexico</h3>
                            </div>
                            <table class="w-full">
                                <thead>
                                    <tr class="border-b border-slate-200">
                                        <th class="px-6 py-4 text-left text-[10px] font-bold uppercase text-slate-400">Treatment</th>
                                        <th class="px-6 py-4 text-center text-[10px] font-bold uppercase text-slate-400">US Average</th>
                                        <th class="px-6 py-4 text-center text-[10px] font-bold uppercase text-slate-400">Mexico Average</th>
                                        <th class="px-6 py-4 text-right text-[10px] font-bold uppercase text-slate-400">Savings</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-slate-100">
                                    <template x-for="item in comparisons" :key="item.treatment">
                                        <tr class="hover:bg-brand-50/30 transition">
                                            <td class="px-6 py-4 font-bold text-slate-900" x-text="item.treatment"></td>
                                            <td class="px-6 py-4 text-center text-slate-500" x-text="item.us"></td>
                                            <td class="px-6 py-4 text-center font-bold text-emerald-600" x-text="item.mexico"></td>
                                            <td class="px-6 py-4 text-right">
                                                <span class="px-2 py-1 bg-emerald-100 text-emerald-700 rounded text-xs font-bold" x-text="item.savings"></span>
                                            </td>
                                        </tr>
                                    </template>
                                </tbody>
                            </table>
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                            <div @click="$dispatch('navigate', 'mexico-clinic')" class="bg-white rounded-3xl p-6 border border-slate-200 hover:shadow-xl hover:-translate-y-1 transition-all cursor-pointer group">
                                <h3 class="text-xl font-extrabold text-slate-900 mb-2 group-hover:text-brand-600">Tijuana Clinics</h3>
                                <p class="text-sm text-slate-500 mb-4">15 verified clinics | Avg $2,800</p>
                                <span class="text-xs font-bold text-brand-600">View All &rarr;</span>
                            </div>
                            <div class="bg-white rounded-3xl p-6 border border-slate-200 hover:shadow-xl hover:-translate-y-1 transition-all cursor-pointer group">
                                <h3 class="text-xl font-extrabold text-slate-900 mb-2 group-hover:text-brand-600">Cancun Clinics</h3>
                                <p class="text-sm text-slate-500 mb-4">8 verified clinics | Avg $3,200</p>
                                <span class="text-xs font-bold text-brand-600">View All &rarr;</span>
                            </div>
                            <div class="bg-white rounded-3xl p-6 border border-slate-200 hover:shadow-xl hover:-translate-y-1 transition-all cursor-pointer group">
                                <h3 class="text-xl font-extrabold text-slate-900 mb-2 group-hover:text-brand-600">Puerto Vallarta</h3>
                                <p class="text-sm text-slate-500 mb-4">6 verified clinics | Avg $3,000</p>
                                <span class="text-xs font-bold text-brand-600">View All &rarr;</span>
                            </div>
                        </div>

                        <div class="mt-12 p-6 bg-amber-50 rounded-2xl border border-amber-200">
                            <div class="flex items-start gap-4">
                                <svg class="w-6 h-6 text-amber-600 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                                <div>
                                    <h4 class="font-bold text-amber-800 mb-1">Important: Medical Tourism Considerations</h4>
                                    <p class="text-sm text-amber-700">Prices shown do not include travel, lodging, or follow-up care. Some treatments offered in Mexico may not be FDA-approved for use in the United States. Always verify clinic credentials and treatment protocols before traveling.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            `;
        }
    };
}

// Mexico Clinic Page
function mexicoClinicPage() {
    return {
        treatments: [
            { name: 'IV Stem Cell Infusion', price: '$4,500', details: 'High-dose expanded MSCs' },
            { name: 'Knee Injection (Both)', price: '$4,200', details: 'BMAC or culture-expanded' },
            { name: 'Full Body Protocol', price: '$12,000', details: 'IV + Joint + Facial' }
        ],

        init() {
            this.$nextTick(() => this.renderContent());
        },

        renderContent() {
            this.$el.innerHTML = `
                <section class="bg-white border-b border-slate-200 py-8 lg:py-12">
                    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <nav class="flex text-xs font-bold text-slate-400 uppercase tracking-widest mb-6 gap-2 items-center">
                            <a href="#" @click.prevent="$dispatch('navigate', 'mexico-comparison')" class="hover:text-brand-600">Mexico</a>
                            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"></path></svg>
                            <span class="text-slate-600">Tijuana</span>
                        </nav>
                        <div class="flex items-center gap-3 mb-3">
                            <span class="px-2.5 py-1 bg-emerald-600 text-white text-[10px] font-black uppercase rounded">International</span>
                            <span class="text-emerald-600 bg-emerald-50 px-2 py-1 rounded text-xs font-bold border border-emerald-100">All-Inclusive Packages</span>
                        </div>
                        <h1 class="text-3xl md:text-5xl font-extrabold text-slate-900 tracking-tight mb-2">
                            BioXcellerator Tijuana
                        </h1>
                        <p class="flex items-center gap-1.5 font-medium text-slate-500">
                            <svg class="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path></svg>
                            Zona Rio, Tijuana, Baja California, Mexico
                        </p>
                    </div>
                </section>

                <section class="py-12">
                    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div class="grid grid-cols-1 lg:grid-cols-12 gap-12">
                            <div class="lg:col-span-8">
                                <div class="bg-white rounded-3xl border border-slate-200 overflow-hidden mb-12">
                                    <div class="p-6 border-b border-slate-100 bg-slate-50/50">
                                        <h3 class="font-extrabold text-lg">Treatment Packages</h3>
                                    </div>
                                    <div class="divide-y divide-slate-100">
                                        <template x-for="item in treatments" :key="item.name">
                                            <div class="p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4 hover:bg-slate-50 transition">
                                                <div>
                                                    <h4 class="font-bold text-slate-900" x-text="item.name"></h4>
                                                    <p class="text-xs text-slate-500" x-text="item.details"></p>
                                                </div>
                                                <div class="flex flex-col sm:items-end">
                                                    <span class="text-xl font-extrabold text-emerald-600" x-text="item.price"></span>
                                                    <span class="text-[10px] font-bold text-slate-400 uppercase">USD Package Price</span>
                                                </div>
                                            </div>
                                        </template>
                                    </div>
                                </div>

                                <div class="bg-brand-50 rounded-3xl p-8 border border-brand-100">
                                    <h3 class="font-extrabold text-lg text-slate-900 mb-4">Package Includes</h3>
                                    <ul class="space-y-3">
                                        <li class="flex items-center gap-3 text-sm text-slate-700">
                                            <svg class="w-5 h-5 text-brand-600" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>
                                            Airport pickup and return (San Diego or Tijuana)
                                        </li>
                                        <li class="flex items-center gap-3 text-sm text-slate-700">
                                            <svg class="w-5 h-5 text-brand-600" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>
                                            All lab work and imaging
                                        </li>
                                        <li class="flex items-center gap-3 text-sm text-slate-700">
                                            <svg class="w-5 h-5 text-brand-600" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>
                                            Post-procedure monitoring
                                        </li>
                                    </ul>
                                </div>
                            </div>

                            <div class="lg:col-span-4">
                                <div class="sticky sticky-sidebar bg-white rounded-3xl p-6 border border-slate-200 shadow-xl">
                                    <h3 class="font-extrabold text-xl mb-6">Request Information</h3>
                                    <button class="w-full bg-emerald-600 text-white py-4 rounded-2xl font-bold hover:bg-emerald-700 transition-all mb-3">
                                        WhatsApp Inquiry
                                    </button>
                                    <button class="w-full bg-white text-slate-700 border-2 border-slate-100 py-4 rounded-2xl font-bold hover:border-brand-200 transition-all">
                                        Email Clinic
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            `;
        }
    };
}
