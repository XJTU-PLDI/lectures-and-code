#import "@preview/touying:0.6.1": *
#import themes.metropolis: *
#import "@preview/numbly:0.1.0": numbly

#show: metropolis-theme.with(
    aspect-ratio: "16-9",
    // config-common(handout: true),
    config-info(
    title: [花2小时实现一门简单的编程语言],
    subtitle: [],
    author: [MikanAffine],
    date: datetime.today(),
    institution: [XJTU PLDI Group],
    logo: emoji.school,
    ),
)

#set heading(numbering: numbly("{1}.", default: "1.1"))

#title-slide()

== Outline <touying:hidden>

#components.adaptive-columns(outline(title: none, indent: 1em))

#show: appendix

= Appendix

== Appendix

Please pay attention to the current slide number.
