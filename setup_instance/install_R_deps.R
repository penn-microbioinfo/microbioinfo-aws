cran_deps = c('tidyverse', 'Seurat', 'remotes', 'future')

for (d in cran_deps) {
    if (!requireNamespace(d, quietly=T)) {
        install.packages(d)
    }
}

github_deps = c("mojaveazure/seurat-disk")

for (d in github_deps) {
    if (!requireNamespace(d, quietly=T)) {
        remotes::install_github(d)
    }
}
