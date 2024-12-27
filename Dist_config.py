from scipy import stats
from typing import List, Tuple, Any
from dataclasses import dataclass


@dataclass
class Distribution:
    name: str
    params: List[str]
    initial_values: List[float]
    view_range: Tuple[float, float]
    dist: Any
    pdf: str = '' 
    cdf: str = ''  
    pmf: str = '' 
    is_discrete: bool = False

DISTRIBUTIONS = {
    'normal': Distribution(
        name='Normal (Bell Curve)',
        params=['Mean (center)', 'Standard Deviation (spread)'],
        initial_values=[0, 1],
        view_range=(-5, 5),
        dist=stats.norm,
        pdf=r'$$ f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x - \mu)^2}{2\sigma^2}} $$',
        cdf=r'$$ F(x) = \frac{1}{2} \left[ 1 + \text{erf}\left( \frac{x - \mu}{\sigma \sqrt{2}} \right) \right] $$'
    ),
    'uniform': Distribution(
        name='Uniform (Equal Probability)',
        params=['Minimum Value', 'Maximum Value'],
        initial_values=[0, 10],
        view_range=(-2, 12),
        dist=stats.uniform,
        pdf=r'$$ f(x) = \frac{1}{b - a}, \quad \text{for} \, a \leq x \leq b $$',
        cdf=r'$$ F(x) = \frac{x - a}{b - a}, \quad \text{for} \, a \leq x \leq b $$'
    ),
    'exponential': Distribution(
        name='Exponential (Time Between Events)',
        params=['Rate (λ) - How quickly it decays'],
        initial_values=[1],
        view_range=(0, 10),
        dist=stats.expon,
        pdf=r'$$ f(x) = \lambda e^{-\lambda x}, \quad x \geq 0 $$',
        cdf=r'$$ F(x) = 1 - e^{-\lambda x}, \quad x \geq 0 $$'
    ),
    'poisson': Distribution(
        name='Poisson (Count of Events)',
        params=['Rate (λ) - Average number of events'],
        initial_values=[5],
        view_range=(0, 15),
        dist=stats.poisson,
        pmf=r'$$ P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}, \quad k = 0, 1, 2, \dots $$',
        cdf=r'$$ F(x) = P(X \leq x) $$'  # CDF for Poisson
    ),
    'gamma': Distribution(
        name='Gamma (Waiting Time)',
        params=['Shape (k) - Number of events', 'Scale (θ) - Time between events'],
        initial_values=[2, 2],
        view_range=(0, 10),
        dist=stats.gamma,
        pdf=r'$$ f(x) = \frac{x^{k-1} e^{-x/\theta}}{\theta^k \Gamma(k)}, \quad x \geq 0 $$',
        cdf=r'$$ F(x) = \frac{\gamma(k, x/\theta)}{\Gamma(k)} $$'
    ),
    'beta': Distribution(
        name='Beta (Probability Distribution)',
        params=['Alpha (α) - Success shape', 'Beta (β) - Failure shape'],
        initial_values=[2, 5],
        view_range=(0, 1),
        dist=stats.beta,
        pdf=r'$$ f(x) = \frac{x^{\alpha-1} (1 - x)^{\beta-1}}{B(\alpha, \beta)}, \quad 0 \leq x \leq 1 $$',
        cdf=r'$$ F(x) = I_x(\alpha, \beta) $$'
    ),
    'student_t': Distribution(
        name='Student\'s t (Small Sample Sizes)',
        params=['Degrees of Freedom (Sample size - 1)'],
        initial_values=[5],
        view_range=(-5, 5),
        dist=stats.t,
        pdf=r'$$ f(x) = \frac{\Gamma\left(\frac{\nu+1}{2}\right)}{\sqrt{\nu\pi} \Gamma\left(\frac{\nu}{2}\right)} \left( 1 + \frac{x^2}{\nu} \right)^{-\frac{\nu+1}{2}} $$',
        cdf=r'$$ F(x) = \int_{-\infty}^x f(t) dt $$'
    ),
    'f': Distribution(
        name='F (Comparing Variances)',
        params=['Group 1 Degrees of Freedom', 'Group 2 Degrees of Freedom'],
        initial_values=[5, 10],
        view_range=(0, 5),
        dist=stats.f,
        pdf=r'$$ f(x) = \frac{\Gamma\left(\frac{d_1 + d_2}{2}\right)}{\Gamma\left(\frac{d_1}{2}\right)\Gamma\left(\frac{d_2}{2}\right)} \left( \frac{d_1}{d_2} \right)^{\frac{d_1}{2}} \frac{x^{\frac{d_1}{2}-1}}{\left( 1 + \frac{d_1}{d_2}x \right)^{\frac{d_1+d_2}{2}}} $$',
        cdf=r'$$ F(x) = P(X \leq x) $$'
    ),
    'chi2': Distribution(
        name='Chi-squared (Variance Measure)',
        params=['Degrees of Freedom (Number of categories - 1)'],
        initial_values=[3],
        view_range=(0, 15),
        dist=stats.chi2,
        pdf=r'$$ f(x) = \frac{x^{\frac{d}{2}-1} e^{-x/2}}{2^{d/2} \Gamma\left(\frac{d}{2}\right)}, \quad x \geq 0 $$',
        cdf=r'$$ F(x) = \frac{\gamma\left(\frac{d}{2}, \frac{x}{2}\right)}{\Gamma\left(\frac{d}{2}\right)} $$'
    ),
}

