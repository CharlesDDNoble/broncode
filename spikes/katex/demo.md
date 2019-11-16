**Result** Katex is an efficient way to render Latex equations to HTML.

**Proof** Let's explore some of the cool things we can do in with Katex:

1.  We can represent integrals with nicely formed sub/superscripts
    ```katex
        f(x) = \int_{0}^{\infty}xdt
    ```

    f(x) = \int_{0}^{\infty}xdt

2.  We can do fractions!
    ```katex
        g(x) = \frac{-99y}{100x^{2}}
    ```

    g(x) = \frac{-99y}{100x^{2}}

3.  Support for nested sub/superscripts!
    ```katex
        2^{2^{2^{2}}} = 2^{2^{4}} = 2^{16} \ge 16^{2}
    ```

    2^{2^{2^{2}}} = 2^{2^{4}} = 2^{16} \ge 16^{2}

4.  We've got access to many common math symbols!  
    ```katex
       e = \sum_{k=0}^{\infty}\frac{1}{k!} \approx 2.71
    ```

    e = \sum_{k=0}^{\infty}\frac{1}{k!} \approx 2.71

5.  How about matrices? Yes, sir!
    ```katex
        \begin{vmatrix}
           a & b \\
           c & d
        \end{vmatrix}
    ```

    \begin{vmatrix}   
       a & b \\   
       c & d   
    \end{vmatrix}

5.  Can we align equations? You betcha!
    ```katex
        \begin{aligned}
           a&=b+c \\
           d+e&=f
        \end{aligned}
    ```

    \begin{aligned}   
       a&=b+c \\   
       d+e&=f   
    \end{aligned}


In summary, katex + showdown = extremely flexible formatting for html and text!