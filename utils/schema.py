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


def doctor_schema(doctor):

    schema = {
        "@context": "https://schema.org",
        "@type": "Physician",
        "name": f"Dr. {doctor.user.first_name} {doctor.user.last_name}",
        "medicalSpecialty": doctor.specialization.name,
        "url": doctor.get_absolute_url() if hasattr(doctor, "get_absolute_url") else "",
        "worksFor": {
            "@type": "Hospital",
            "name": doctor.branch.name
        },
        "description": doctor.short_bio[:200] if doctor.short_bio else ""
    }

    if doctor.profile_image:
        schema["image"] = doctor.profile_image.url

    return schema