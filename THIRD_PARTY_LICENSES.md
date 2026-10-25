# THIRD PARTY LICENSES

This software includes or depends on third-party packages. The following notices are provided to comply with the applicable license requirements of those packages.

The names, trademarks, and project identifiers of third-party software are used solely for attribution and identification purposes. Their inclusion does not imply any affiliation with, sponsorship by, or endorsement from the respective authors or copyright holders.

For the most current information, please refer to the original project repositories and license files.

Byron itself is distributed under the Apache License, Version 2.0 (see `LICENSE`). Apart from the components listed in the first section, Byron does not include third-party code: the packages listed in the other sections are installed separately from their own distributions, which contain their complete license files. Versions are those locked in `uv.lock` when this file was last updated.

## Components included in this repository

### Randy

- URL: https://github.com/squillero/randy
- Version: bundled in `src/byron/randy/`
- License: 0BSD

Randy, the random number generator in `src/byron/randy/main.py`, is written by Byron's author and is distributed under the BSD Zero Clause License.

> Copyright (c) 2023 by Giovanni Squillero <giovanni.squillero@polito.it>
>
> Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted.
>
> THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

### Cayman theme for GitHub Pages

- URL: https://github.com/pages-themes/cayman
- Version: v0.2.0
- License: CC0-1.0

The documentation site uses the Cayman theme (`docs/_config.yml`), and `docs/_layouts/default.html` is a modified copy of its layout. The theme is dedicated to the public domain under CC0 1.0 Universal, which imposes no conditions: https://creativecommons.org/publicdomain/zero/1.0/legalcode

## Required dependencies

### networkx

- URL: https://pypi.org/project/networkx/
- Version: 3.7
- License: BSD-3-Clause

> NetworkX is distributed with the 3-clause BSD license.
>
> ::
>
> Copyright (c) 2004-2026, NetworkX Developers
>
> Aric Hagberg <hagberg@lanl.gov> Dan Schult <dschult@colgate.edu> Pieter Swart <swart@lanl.gov> All rights reserved.
>
> Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
>
> * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
> * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
> * Neither the name of the NetworkX Developers nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
>
> THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

### numpy

- URL: https://pypi.org/project/numpy/
- Version: 2.5.4
- License: BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0

NumPy also contains code distributed under the other licenses listed above. Its binary wheels bundle, depending on the platform, OpenBLAS (BSD-3-Clause), LAPACK (BSD-3-Clause-Open-MPI), the GCC runtime library (GPL-3.0-or-later WITH GCC-exception-3.1) and libquadmath (LGPL-2.1-or-later). Their complete license texts are in the `licenses` folder of the installed package metadata (`numpy-*.dist-info/licenses/`).

> Copyright (c) 2005-2025, NumPy Developers. All rights reserved.
>
> Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
>
> * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
> * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
> * Neither the name of the NumPy Developers nor the names of any contributors may be used to endorse or promote products derived from this software without specific prior written permission.
>
> THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

### rich

- URL: https://pypi.org/project/rich/
- Version: 15.0.0
- License: MIT

> Copyright (c) 2020 Will McGugan
>
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

### scipy

- URL: https://pypi.org/project/scipy/
- Version: 1.18.1
- License: BSD-3-Clause

SciPy also contains code distributed under other compatible licenses, such as Qhull (Qhull license) and several BSD-style components. Its binary wheels bundle, depending on the platform, OpenBLAS (BSD-3-Clause), LAPACK (BSD-3-Clause-Open-MPI), the GCC runtime library (GPL-3.0-or-later WITH GCC-exception-3.1) and libquadmath (LGPL-2.1-or-later). Their complete license texts are in `scipy-*.dist-info/LICENSE.txt` and in the license files of its subpackages.

> Copyright (c) 2001-2002 Enthought, Inc. 2003, SciPy Developers. All rights reserved.
>
> Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
>
> 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
> 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
> 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
>
> THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

### tqdm

- URL: https://pypi.org/project/tqdm/
- Version: 4.70.1
- License: MPL-2.0 AND MIT

> `tqdm` is a product of collaborative work. Unless otherwise stated, all authors (see commit logs) retain copyright for their respective work, and release the work under the MIT licence (text below).
>
> Exceptions or notable authors are listed below in reverse chronological order:
>
> * files: * MPL-2.0 2015-2026 (c) Casper da Costa-Luis [casperdcl](https://github.com/casperdcl).
> * files: tqdm/_tqdm.py MIT 2016 (c) [PR #96] on behalf of Google Inc.
> * files: tqdm/_tqdm.py README.rst .gitignore MIT 2013 (c) Noam Yorav-Raphael, original author.
>
> [PR #96]: https://github.com/tqdm/tqdm/pull/96
>
> Mozilla Public Licence (MPL) v. 2.0 - Exhibit A
>
> -----------------------------------------------
>
> This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed with this project, You can obtain one at https://mozilla.org/MPL/2.0/.
>
> MIT License (MIT)
>
> -----------------
>
> Copyright (c) 2013 noamraph
>
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

The following packages are installed as dependencies of the packages above.

### markdown-it-py

- URL: https://pypi.org/project/markdown-it-py/
- Version: 4.2.0
- License: MIT

> MIT License
>
> Copyright (c) 2020 ExecutableBookProject
>
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

> Copyright (c) 2014 Vitaly Puzrin, Alex Kocharin.
>
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

### mdurl

- URL: https://pypi.org/project/mdurl/
- Version: 0.1.2
- License: MIT

> Copyright (c) 2015 Vitaly Puzrin, Alex Kocharin.
>
> Copyright (c) 2021 Taneli Hukkinen
>
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
>
> --------------------------------------------------------------------------------
>
> .parse() is based on Joyent's node.js `url` code:
>
> Copyright Joyent, Inc. and other Node contributors. All rights reserved.
>
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

### Pygments

- URL: https://pypi.org/project/pygments/
- Version: 2.21.0
- License: BSD-2-Clause

The `AUTHORS` file referenced below is included in the installed package (`pygments-*.dist-info/licenses/AUTHORS`).

> Copyright (c) 2006-2022 by the respective authors (see AUTHORS file). All rights reserved.
>
> Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
>
> * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
> * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
>
> THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

### colorama

- URL: https://pypi.org/project/colorama/
- Version: 0.4.6
- License: BSD-3-Clause

Installed on Windows only, as a dependency of tqdm.

> Copyright (c) 2010 Jonathan Hartley All rights reserved.
>
> Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
>
> * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
> * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
> * Neither the name of the copyright holders, nor those of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
>
> THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## Optional dependencies (`byron[all]`)

### joblib

- URL: https://pypi.org/project/joblib/
- Version: 1.6.0
- License: BSD-3-Clause

> BSD 3-Clause License
>
> Copyright (c) 2008-2021, The joblib developers. All rights reserved.
>
> Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
>
> * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
> * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
> * Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
>
> THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

### matplotlib

- URL: https://pypi.org/project/matplotlib/
- Version: 3.11.2
- License: Matplotlib License (PSF-based)

The license file also contains the agreement for versions prior to 1.3.0. Matplotlib bundles, depending on the build, AMS, Last Resort and STIX fonts (OFL-1.1), BaKoMa fonts (BaKoMa Fonts Licence), ColorBrewer color schemes (Apache-2.0), Courier 10 (Bitstream-Charter), FreeType (FTL OR GPL-2.0-or-later), HarfBuzz (MIT-Modern-Variant), JSXTools resize observer (CC0-1.0), libraqm (MIT), Qhull (Qhull), Qt4 Editor (MIT), SheenBidi (Apache-2.0) and Solarized (MIT). Their complete license texts are in `matplotlib-*.dist-info/LICENSE`.

> License agreement for matplotlib versions 1.3.0 and later
>
> =========================================================
>
> 1. This LICENSE AGREEMENT is between the Matplotlib Development Team ("MDT"), and the Individual or Organization ("Licensee") accessing and otherwise using matplotlib software in source or binary form and its associated documentation.
> 2. Subject to the terms and conditions of this License Agreement, MDT hereby grants Licensee a nonexclusive, royalty-free, world-wide license to reproduce, analyze, test, perform and/or display publicly, prepare derivative works, distribute, and otherwise use matplotlib alone or in any derivative version, provided, however, that MDT's License Agreement and MDT's notice of copyright, i.e., "Copyright (c) 2012- Matplotlib Development Team; All Rights Reserved" are retained in matplotlib  alone or in any derivative version prepared by Licensee.
> 3. In the event Licensee prepares a derivative work that is based on or incorporates matplotlib or any part thereof, and wants to make the derivative work available to others as provided herein, then Licensee hereby agrees to include in any such work a brief summary of the changes made to matplotlib .
> 4. MDT is making matplotlib available to Licensee on an "AS IS" basis.  MDT MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR IMPLIED.  BY WAY OF EXAMPLE, BUT NOT LIMITATION, MDT MAKES NO AND DISCLAIMS ANY REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR FITNESS FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF MATPLOTLIB WILL NOT INFRINGE ANY THIRD PARTY RIGHTS.
> 5. MDT SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF MATPLOTLIB FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS AS A RESULT OF MODIFYING, DISTRIBUTING, OR OTHERWISE USING MATPLOTLIB , OR ANY DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.
> 6. This License Agreement will automatically terminate upon a material breach of its terms and conditions.
> 7. Nothing in this License Agreement shall be deemed to create any relationship of agency, partnership, or joint venture between MDT and Licensee.  This License Agreement does not grant permission to use MDT trademarks or trade name in a trademark sense to endorse or promote products or services of Licensee, or any third party.
> 8. By copying, installing or otherwise using matplotlib , Licensee agrees to be bound by the terms and conditions of this License Agreement.

### psutil

- URL: https://pypi.org/project/psutil/
- Version: 7.2.2
- License: BSD-3-Clause

> BSD 3-Clause License
>
> Copyright (c) 2009, Jay Loden, Dave Daeschler, Giampaolo Rodola All rights reserved.
>
> Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
>
> * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
> * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
> * Neither the name of the psutil authors nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
>
> THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The following packages are installed as dependencies of the optional packages above.

### cloudpickle

- URL: https://pypi.org/project/cloudpickle/
- Version: 3.1.2
- License: BSD-3-Clause

> This module was extracted from the `cloud` package, developed by PiCloud, Inc.
>
> Copyright (c) 2015, Cloudpickle contributors.
>
> Copyright (c) 2012, Regents of the University of California.
>
> Copyright (c) 2009 PiCloud, Inc. http://www.picloud.com. All rights reserved.
>
> Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
>
> * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
> * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
> * Neither the name of the University of California, Berkeley nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
>
> THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

### contourpy

- URL: https://pypi.org/project/contourpy/
- Version: 1.4.0
- License: BSD-3-Clause

> BSD 3-Clause License
>
> Copyright (c) 2021-2026, ContourPy Developers. All rights reserved.
>
> Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
>
> 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
> 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
> 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
>
> THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

### cycler

- URL: https://pypi.org/project/cycler/
- Version: 0.12.1
- License: BSD-3-Clause

> Copyright (c) 2015, matplotlib project All rights reserved.
>
> Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
>
> * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
> * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
> * Neither the name of the matplotlib project nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
>
> THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

### fontTools

- URL: https://pypi.org/project/fonttools/
- Version: 4.67.0
- License: MIT

fontTools also includes test fonts under OFL-1.1 (Lobster, Noto, XITS, Iosevka), Adobe AGL and AGLFN (BSD-3-Clause), cu2qu (Apache-2.0, Copyright 2016 Google Inc.) and code derived from PyFilesystem2 (MIT). Their notices are in `fonttools-*.dist-info/licenses/LICENSE.external`.

> MIT License
>
> Copyright (c) 2017 Just van Rossum
>
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

### kiwisolver

- URL: https://pypi.org/project/kiwisolver/
- Version: 1.5.1
- License: BSD-3-Clause

> =========================
>
> The Kiwi licensing terms
>
> =========================
>
> Kiwi is licensed under the terms of the Modified BSD License (also known as New or Revised BSD), as follows:
>
> Copyright (c) 2013-2026, Nucleic Development Team
>
> All rights reserved.
>
> Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
>
> Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
>
> Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
>
> Neither the name of the Nucleic Development Team nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
>
> THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
>
> About Kiwi
>
> ----------
>
> Chris Colbert began the Kiwi project in December 2013 in an effort to create a blisteringly fast UI constraint solver. Chris is still the project lead.
>
> The Nucleic Development Team is the set of all contributors to the Nucleic project and its subprojects.
>
> The core team that coordinates development on GitHub can be found here: http://github.com/nucleic. The current team consists of:
>
> * Chris Colbert
>
> Our Copyright Policy
>
> --------------------
>
> Nucleic uses a shared copyright model. Each contributor maintains copyright over their contributions to Nucleic. But, it is important to note that these contributions are typically only changes to the repositories. Thus, the Nucleic source code, in its entirety is not the copyright of any single person or institution. Instead, it is the collective copyright of the entire Nucleic Development Team. If individual contributors want to maintain a record of what changes/contributions they have specific copyright on, they should indicate their copyright in the commit message of the change, when they commit the change to one of the Nucleic repositories.
>
> With this in mind, the following banner should be used in any source code file to indicate the copyright and license terms:
>
> ```text
> #------------------------------------------------------------------------------
> # Copyright (c) 2013-2026, Nucleic Development Team.
> #
> # Distributed under the terms of the Modified BSD License.
> #
> # The full license is in the file LICENSE, distributed with this software.
> #------------------------------------------------------------------------------
> ```

### packaging

- URL: https://pypi.org/project/packaging/
- Version: 26.3
- License: Apache-2.0 OR BSD-2-Clause

The full text of the Apache License, Version 2.0 is in the `LICENSE` file of this repository.

> This software is made available under the terms of *either* of the licenses found in LICENSE.APACHE or LICENSE.BSD. Contributions to this software is made under the terms of *both* these licenses.

> Copyright (c) Donald Stufft and individual contributors. All rights reserved.
>
> Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
>
> 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
> 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
>
> THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

### Pillow

- URL: https://pypi.org/project/pillow/
- Version: 13.0.0
- License: MIT-CMU

Pillow's binary wheels bundle AOM, Brotli, bzip2, dav1d, FreeType, HarfBuzz, Little CMS, libavif, libjpeg, liblzma, libpng, LibTIFF, libwebp, libyuv, OpenJPEG, Raqm, Tcl/Tk, libXau, libxcb, libXdmcp, zlib and Zstandard, each under its own license. Their complete license texts are in `pillow-*.dist-info/licenses/LICENSE`.

> The Python Imaging Library (PIL) is
>
> Copyright © 1997-2011 by Secret Labs AB
>
> Copyright © 1995-2011 by Fredrik Lundh and contributors
>
> Pillow is the friendly PIL fork. It is
>
> Copyright © 2010 by Jeffrey 'Alex' Clark and contributors
>
> Like PIL, Pillow is licensed under the open source MIT-CMU License:
>
> By obtaining, using, and/or copying this software and/or its associated documentation, you agree that you have read, understood, and will comply with the following terms and conditions:
>
> Permission to use, copy, modify and distribute this software and its documentation for any purpose and without fee is hereby granted, provided that the above copyright notice appears in all copies, and that both that copyright notice and this permission notice appear in supporting documentation, and that the name of Secret Labs AB or the author not be used in advertising or publicity pertaining to distribution of the software without specific, written prior permission.
>
> SECRET LABS AB AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL SECRET LABS AB OR THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

### pyparsing

- URL: https://pypi.org/project/pyparsing/
- Version: 3.3.3
- License: MIT

> Copyright (c) 2003-2025  Paul McGuire
>
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

### python-dateutil

- URL: https://pypi.org/project/python-dateutil/
- Version: 3.0.0
- License: Apache-2.0 AND BSD-3-Clause

The full text of the Apache License, Version 2.0 is in the `LICENSE` file of this repository.

> Copyright 2017- Paul Ganssle <paul@ganssle.io>
>
> Copyright 2017- dateutil contributors (see AUTHORS file)
>
> Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
>
> http://www.apache.org/licenses/LICENSE-2.0
>
> Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
>
> The above license applies to all contributions after 2017-12-01, as well as all contributions that have been re-licensed (see AUTHORS file for the list of contributors who have re-licensed their code).
>
> --------------------------------------------------------------------------------
>
> dateutil - Extensions to the standard Python datetime module.
>
> Copyright (c) 2003-2011 - Gustavo Niemeyer <gustavo@niemeyer.net>
>
> Copyright (c) 2012-2014 - Tomi Pieviläinen <tomi.pievilainen@iki.fi>
>
> Copyright (c) 2014-2016 - Yaron de Leeuw <me@jarondl.net>
>
> Copyright (c) 2015-     - Paul Ganssle <paul@ganssle.io>
>
> Copyright (c) 2015-     - dateutil contributors (see AUTHORS file)
>
> All rights reserved.
>
> Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
>
> * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
> * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
> * Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
>
> THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
>
> The above BSD License Applies to all code, even that also covered by Apache 2.0.

### six

- URL: https://pypi.org/project/six/
- Version: 1.17.0
- License: MIT

> Copyright (c) 2010-2024 Benjamin Peterson
>
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

### tzdata

- URL: https://pypi.org/project/tzdata/
- Version: 2026.5
- License: Apache-2.0

The full text of the Apache License, Version 2.0 is in the `LICENSE` file of this repository.

> Apache Software License 2.0
>
> Copyright (c) 2020, Paul Ganssle (Google)
>
> Copyright (c) 2026, Stan Ulbrych
>
> Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
>
> http://www.apache.org/licenses/LICENSE-2.0
>
> Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

## Packages used when installed

### dill

- URL: https://pypi.org/project/dill/
- Version: not pinned (0.4.1 when this file was written)
- License: BSD-3-Clause

`dill` is not a dependency of Byron. `src/byron/tools/checkpoint.py` uses it instead of `pickle` when it is installed.

> Copyright (c) 2004-2016 California Institute of Technology.
>
> Copyright (c) 2016-2026 The Uncertainty Quantification Foundation. All rights reserved.
>
> This software is available subject to the conditions and terms laid out below. By downloading and using this software you are agreeing to the following conditions.
>
> Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
>
> - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
> - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
> - Neither the names of the copyright holders nor the names of any of the contributors may be used to endorse or promote products derived from this software without specific prior written permission.
>
> THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## Development tools (`dev` dependency group)

These packages are used to develop and test Byron and are not needed to use it.

### icecream

- URL: https://pypi.org/project/icecream/
- Version: 2.2.0
- License: MIT

`src/byron/__init__.py` also imports icecream, if it is installed, to ease debugging.

> Copyright 2018 Ansgar Grunseid
>
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

### asttokens

- URL: https://pypi.org/project/asttokens/
- Version: 3.0.2
- License: Apache-2.0

Installed as a dependency of icecream. Its license file contains the standard text of the Apache License, Version 2.0, without a separate copyright notice; the package metadata names Dmitry Sagalovskiy, Grist Labs as author. The full text of the Apache License, Version 2.0 is in the `LICENSE` file of this repository.

### executing

- URL: https://pypi.org/project/executing/
- Version: 2.3.0
- License: MIT

Installed as a dependency of icecream.

> MIT License
>
> Copyright (c) 2019 Alex Hall
>
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

### pytest

- URL: https://pypi.org/project/pytest/
- Version: 9.1.1
- License: MIT

> The MIT License (MIT)
>
> Copyright (c) 2004 Holger Krekel and others
>
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

### iniconfig

- URL: https://pypi.org/project/iniconfig/
- Version: 2.3.1
- License: MIT

Installed as a dependency of pytest.

> The MIT License (MIT)
>
> Copyright (c) 2010 - 2023 Holger Krekel and others
>
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

### pluggy

- URL: https://pypi.org/project/pluggy/
- Version: 1.7.0
- License: MIT

Installed as a dependency of pytest.

> The MIT License (MIT)
>
> Copyright (c) 2015 holger krekel (rather uses bitbucket/hpk42)
>
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

### pytest-emoji

- URL: https://pypi.org/project/pytest-emoji/
- Version: 0.2.0
- License: MIT

> The MIT License (MIT)
>
> Copyright (c) 2016 Raphael Pierzina
>
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

### Coverage.py

- URL: https://pypi.org/project/coverage/
- Version: 7.17.0
- License: Apache-2.0

The notice below is the `NOTICE` file of the package. The full text of the Apache License, Version 2.0 is in the `LICENSE` file of this repository.

> Copyright 2001 Gareth Rees.  All rights reserved.
>
> Copyright 2004-2026 Ned Batchelder.  All rights reserved.
>
> Except where noted otherwise, this software is licensed under the Apache License, Version 2.0 (the "License"); you may not use this work except in compliance with the License.  You may obtain a copy of the License at
>
> http://www.apache.org/licenses/LICENSE-2.0
>
> Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

### jupyter

- URL: https://pypi.org/project/jupyter/
- Version: 1.1.1
- License: BSD-3-Clause

> BSD 3-Clause License
>
> Copyright (c) 2017, Project Jupyter Contributors All rights reserved.
>
> Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
>
> * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
> * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
> * Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
>
> THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

### Other packages installed by the `dev` group

The `jupyter` package installs the following packages, some of them only on specific platforms. The licenses are those declared by each package; see its distribution for the complete license text.

| Package | Version | License |
| --- | --- | --- |
| [anyio](https://pypi.org/project/anyio/) | 4.15.1 | MIT |
| [appnope](https://pypi.org/project/appnope/) | 1.0.0 | BSD-2-Clause |
| [argon2-cffi](https://pypi.org/project/argon2-cffi/) | 25.1.0 | MIT |
| [argon2-cffi-bindings](https://pypi.org/project/argon2-cffi-bindings/) | 26.1.0 | MIT |
| [async-lru](https://pypi.org/project/async-lru/) | 2.4.0 | MIT |
| [attrs](https://pypi.org/project/attrs/) | 26.1.0 | MIT |
| [babel](https://pypi.org/project/babel/) | 2.18.0 | BSD-3-Clause |
| [beautifulsoup4](https://pypi.org/project/beautifulsoup4/) | 4.15.0 | MIT |
| [bleach](https://pypi.org/project/bleach/) | 6.4.0 | Apache-2.0 |
| [certifi](https://pypi.org/project/certifi/) | 2026.10.23 | MPL-2.0 |
| [cffi](https://pypi.org/project/cffi/) | 2.1.1 | MIT-0 |
| [charset-normalizer](https://pypi.org/project/charset-normalizer/) | 3.5.2 | MIT |
| [comm](https://pypi.org/project/comm/) | 0.2.3 | BSD-3-Clause |
| [debugpy](https://pypi.org/project/debugpy/) | 1.8.22 | MIT |
| [defusedxml](https://pypi.org/project/defusedxml/) | 0.7.1 | PSF-2.0 |
| [fastjsonschema](https://pypi.org/project/fastjsonschema/) | 2.22.2 | BSD-3-Clause |
| [h11](https://pypi.org/project/h11/) | 0.16.0 | MIT |
| [httpcore](https://pypi.org/project/httpcore/) | 1.0.9 | BSD-3-Clause |
| [httpx](https://pypi.org/project/httpx/) | 0.28.1 | BSD-3-Clause |
| [idna](https://pypi.org/project/idna/) | 3.20 | BSD-3-Clause |
| [ipykernel](https://pypi.org/project/ipykernel/) | 7.4.0 | BSD-3-Clause |
| [ipython](https://pypi.org/project/ipython/) | 9.17.1 | BSD-3-Clause |
| [ipython-pygments-lexers](https://pypi.org/project/ipython-pygments-lexers/) | 1.1.1 | BSD-3-Clause |
| [ipywidgets](https://pypi.org/project/ipywidgets/) | 8.1.9 | BSD-3-Clause |
| [jedi](https://pypi.org/project/jedi/) | 0.20.1 | MIT |
| [jinja2](https://pypi.org/project/jinja2/) | 3.1.6 | BSD-3-Clause |
| [json5](https://pypi.org/project/json5/) | 0.17.3 | Apache-2.0 |
| [jsonschema](https://pypi.org/project/jsonschema/) | 4.26.0 | MIT |
| [jsonschema-specifications](https://pypi.org/project/jsonschema-specifications/) | 2025.9.1 | MIT |
| [jupyter-builder](https://pypi.org/project/jupyter-builder/) | 1.2.3 | Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND ISC AND MIT |
| [jupyter-client](https://pypi.org/project/jupyter-client/) | 8.10.0 | BSD-3-Clause |
| [jupyter-console](https://pypi.org/project/jupyter-console/) | 6.6.3 | BSD-3-Clause |
| [jupyter-core](https://pypi.org/project/jupyter-core/) | 5.9.1 | BSD-3-Clause |
| [jupyter-events](https://pypi.org/project/jupyter-events/) | 0.12.1 | BSD-3-Clause |
| [jupyter-lsp](https://pypi.org/project/jupyter-lsp/) | 2.3.1 | BSD-3-Clause |
| [jupyter-server](https://pypi.org/project/jupyter-server/) | 2.21.1 | BSD-3-Clause |
| [jupyter-server-terminals](https://pypi.org/project/jupyter-server-terminals/) | 0.5.4 | BSD-3-Clause |
| [jupyterlab](https://pypi.org/project/jupyterlab/) | 4.6.4 | BSD-3-Clause |
| [jupyterlab-pygments](https://pypi.org/project/jupyterlab-pygments/) | 0.3.0 | BSD-3-Clause |
| [jupyterlab-server](https://pypi.org/project/jupyterlab-server/) | 2.28.1 | BSD-3-Clause |
| [jupyterlab-widgets](https://pypi.org/project/jupyterlab-widgets/) | 3.0.17 | BSD-3-Clause |
| [markupsafe](https://pypi.org/project/markupsafe/) | 3.0.4 | BSD-3-Clause |
| [matplotlib-inline](https://pypi.org/project/matplotlib-inline/) | 0.2.2 | BSD-3-Clause |
| [mistune](https://pypi.org/project/mistune/) | 3.4.0 | BSD-3-Clause |
| [nbclient](https://pypi.org/project/nbclient/) | 0.11.0 | BSD-3-Clause |
| [nbconvert](https://pypi.org/project/nbconvert/) | 7.17.2 | BSD-3-Clause |
| [nbformat](https://pypi.org/project/nbformat/) | 5.11.1 | BSD-3-Clause |
| [nest-asyncio2](https://pypi.org/project/nest-asyncio2/) | 1.7.4 | BSD-2-Clause |
| [notebook](https://pypi.org/project/notebook/) | 7.6.3 | BSD-3-Clause |
| [notebook-shim](https://pypi.org/project/notebook-shim/) | 0.2.4 | BSD-3-Clause |
| [pandocfilters](https://pypi.org/project/pandocfilters/) | 1.5.1 | BSD-3-Clause |
| [parso](https://pypi.org/project/parso/) | 0.8.7 | MIT |
| [pexpect](https://pypi.org/project/pexpect/) | 4.9.0 | ISC |
| [platformdirs](https://pypi.org/project/platformdirs/) | 4.13.5 | MIT |
| [prometheus-client](https://pypi.org/project/prometheus-client/) | 0.26.0 | Apache-2.0 AND BSD-2-Clause |
| [prompt-toolkit](https://pypi.org/project/prompt-toolkit/) | 3.0.53 | BSD-3-Clause |
| [ptyprocess](https://pypi.org/project/ptyprocess/) | 0.7.0 | ISC |
| [pure-eval](https://pypi.org/project/pure-eval/) | 0.2.4 | MIT |
| [pycparser](https://pypi.org/project/pycparser/) | 3.12 | BSD-3-Clause |
| [python-json-logger](https://pypi.org/project/python-json-logger/) | 4.2.0 | BSD-2-Clause |
| [pywinpty](https://pypi.org/project/pywinpty/) | 3.1.0 | MIT |
| [pyyaml](https://pypi.org/project/pyyaml/) | 6.0.3 | MIT |
| [pyzmq](https://pypi.org/project/pyzmq/) | 27.2.0 | BSD-3-Clause |
| [referencing](https://pypi.org/project/referencing/) | 0.37.0 | MIT |
| [requests](https://pypi.org/project/requests/) | 2.34.2 | Apache-2.0 |
| [rfc3339-validator](https://pypi.org/project/rfc3339-validator/) | 0.1.4 | MIT |
| [rfc3986-validator](https://pypi.org/project/rfc3986-validator/) | 0.1.1 | MIT |
| [rpds-py](https://pypi.org/project/rpds-py/) | 2026.9.1 | MIT |
| [send2trash](https://pypi.org/project/send2trash/) | 2.1.0 | BSD-3-Clause |
| [soupsieve](https://pypi.org/project/soupsieve/) | 3.0.4 | MIT |
| [stack-data](https://pypi.org/project/stack-data/) | 0.6.3 | MIT |
| [terminado](https://pypi.org/project/terminado/) | 0.18.1 | BSD-2-Clause |
| [tornado](https://pypi.org/project/tornado/) | 6.6 | Apache-2.0 |
| [traitlets](https://pypi.org/project/traitlets/) | 5.16.1 | BSD-3-Clause |
| [typing-extensions](https://pypi.org/project/typing-extensions/) | 4.16.0 | PSF-2.0 |
| [urllib3](https://pypi.org/project/urllib3/) | 2.8.0 | MIT |
| [wcwidth](https://pypi.org/project/wcwidth/) | 0.9.4 | MIT |
| [webencodings](https://pypi.org/project/webencodings/) | 0.6.1 | BSD-3-Clause |
| [websocket-client](https://pypi.org/project/websocket-client/) | 1.9.2 | Apache-2.0 |
| [widgetsnbextension](https://pypi.org/project/widgetsnbextension/) | 4.0.16 | BSD-3-Clause |
