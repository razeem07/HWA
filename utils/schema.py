def specialization_schema(spec):

    schema = {
        "@context": "https://schema.org",
        "@type": "MedicalSpecialty",
        "name": spec.name,
        "description": spec.short_description,
        "url": f"/specializations/{spec.slug}/",
    }

    # add image if available
    if spec.featured_image:
        schema["image"] = spec.featured_image.url

    return schema