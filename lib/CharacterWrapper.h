#ifndef CHARACTER_WRAPPER_H
#define CHARACTER_WRAPPER_H

#include <QObject>
#include <QColor>

class CharacterWrapper
{
public:
    CharacterWrapper() : characterValue_(0), foregroundColor_(QColor()), backgroundColor_(QColor()), rendition_(0) {}
    CharacterWrapper(quint16 characterValue, QColor foregroundColor, QColor backgroundColor, quint8 rendition) :
        characterValue_(characterValue),
        foregroundColor_(foregroundColor),
        backgroundColor_(backgroundColor),
        rendition_(rendition) {}
    
    inline quint16 characterValue() const { return characterValue_; }
    inline QColor foregroundColor() const { return foregroundColor_; }
    inline QColor backgroundColor() const { return backgroundColor_; }
    inline quint8 rendition() const { return rendition_; }

private:
    quint16 characterValue_;
    QColor foregroundColor_;
    QColor backgroundColor_;
    quint8 rendition_;
};

#endif // CHARACTER_WRAPPER_H