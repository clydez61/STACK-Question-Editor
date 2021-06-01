options["grading"]="manual"

question={
    "name": "Absolute Value In Lpp",
    "questiontext": """
Reformulate the problem
\[
\begin{array}{lrcrcr}
\mathrm{minimize} & 2x_1 &+& 3|x_2 &-& @a@| \\
\mathrm{subject\ to\ } & |x_1 + 2| &+& x_2 &\leq& 5,
\end{array}
\]
as a linear programming problem by replacing the argument $x_k$ of each absolute value $|x_k|$ as the difference of two new non-negative decision variables $p_k$ and $m_k$, expressing its absolute value as their sum. Then
put the problem into standard form, by introducing $s$ slack variables $x_k$ as needed, where $k=n+1\ldots n+s$ and $n$ is the number of original decision variables. Please retain all constants in the cost function, so that the standard-form cost agrees with the cost in the original problem.


$\mathrm{minimize}$ [[input:cost]] $\mathrm{subject\ to}$


[[input:constraint]],


[[input:variables]]$\ge\mathbf{0}$,


[[validation:cost]]


[[validation:constraint]]


[[validation:variables]]
""",
    "generalfeedback": """
Let $x_1+2=p_1-m_1$ and replace $|x_1+2|$ by $p_1+m_1$.
Let $x_2-@a@=p_2-m_2$, replacing $|x_2-@a@|$ with
$p_2+m_2$. We obtain the equivalent linear programming problem
\[
\begin{array}{lrcrcrcrcrcr}
\mathrm{minimize}    &2p_1    &-&2m_1    &+&3p_2    &+&3m_2    &-&4  \\
\mathrm{subject\ to}     &p_1    &+&m_1    &+&p_2    &-&m_2  &+&x_3    &=&@5-a@,\\
            &[p_1,\kern-2.78pt&&m_1,\kern-2.78pt&&p_2,\kern-2.78pt&&m_2,\kern-2.78pt&&x_3]&\ge& \mathbf{0}.
\end{array}
\]
""",
    "defaultgrade": "3",
    "penalty": 0.1,
    "stackversion": "2019121800",
    "questionvariables": """
ordergreat(p1,m1,p2,m2,x3);
a:rand_with_step(1,20,1);
_cost:2*p1-2*m1+3*p2+3*m2-4;
_constraint:p1+m1+p2-m2+x3=5-a;
_variables:[p1,m1,p2,m2,x3];
""",
    "specificfeedback": """
[[feedback:prt1]]
[[feedback:constraint]]
[[feedback:variables]]
""",
    "questionnote": """
Variables: a
Any edits should be made to the original source: C:\Users\zhouc\Python_Workspace\tools\examples\absolute-value-in-lpp.py
This question was generated with qcreate version 0.98 from https://gitlab.com/stacktools/tools
""",
    "multiplicationsign": "none",
    "input": [
        {
            "name": "constraint",
            "tans": "_constraint"
        },
        {
            "name": "cost",
            "tans": "_cost"
        },
        {
            "name": "variables",
            "tans": "_variables"
        }
    ],
    "prt": [
        {
            "name": "constraint",
            "node": {
                "name": "0",
                "sans": "constraint",
                "tans": "_constraint",
                "truefeedback": """

constraint: correct
""",
                "falsefeedback": """

constraint: incorrect
"""
            }
        },
        {
            "name": "prt1",
            "node": {
                "name": "0",
                "sans": "simplify(cost-_cost)",
                "tans": "0",
                "truefeedback": """

cost: correct
""",
                "falsefeedback": """

cost: incorrect
"""
            }
        },
        {
            "name": "variables",
            "node": {
                "name": "0",
                "sans": "variables",
                "tans": "_variables",
                "truefeedback": """

variables: correct
""",
                "falsefeedback": """

variables: incorrect
"""
            }
        }
    ],
    "tags": {
        "tag": [
            "tag1",
            "tag2"
        ]
    }
}